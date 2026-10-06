#!/usr/bin/env python3
"""Deterministic routing-table test of the documented boot path.

This is NOT a behavioural test of a real agent: no model runs. It applies the
profile table in AGENTS.md and the pick rule + routing table in skills/INDEX.md
exactly as written, to the tasks in tests/fixtures/standup_tasks.json, so a
broken table, a missing profile or a budget overrun fails. For each task it
records the files a rule-following agent would load and their cl100k token
counts, then asserts the expected profile, expected/forbidden skills and the
stand-up budget. A task with "must_trigger_hitl" also runs the
human-in-the-loop example gate on a send_email action and asserts it never
executes without APPROVE. Whether a real bot follows these rules is untested.

Usage: python3 tools/standup_sim.py [--json]
Exit code 0 when every fixture passes. Needs stdlib + tiktoken.
"""
import importlib.util
import json
import os
import re
import sys

import tiktoken

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, "AGENTS.md")
INDEX = os.path.join(ROOT, "skills", "INDEX.md")
BOOT_FILES = ["AGENTS.md", "skills/INDEX.md"]
FIXTURES = os.path.join(ROOT, "tests", "fixtures", "standup_tasks.json")
MAX_SKILLS = 3
SUFFIX = r"(?:s|es|d|ed|ing)?"
ENC = tiktoken.get_encoding("cl100k_base")


def tokens(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return len(ENC.encode(f.read()))


def table(text, header):
    """Rows of the markdown table whose header cells equal `header`."""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells == header:
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return rows
    raise ValueError(f"table {header} not found")


def parse_standup(agents=AGENTS, index=INDEX):
    with open(agents, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"Stand-up budget: (\d+) tokens", text)
    if not m:
        raise ValueError("AGENTS.md: 'Stand-up budget: N tokens' line not found")
    profiles = [([s.strip().lower() for s in sig.split(",")], prof)
                for sig, prof in table(text, ["runtime signal", "profile"])]
    with open(index, encoding="utf-8") as f:
        idx = f.read()
    routes = [{"id": sid, "role": [r.strip() for r in role.split(",")],
               "signals": [s.strip().lower() for s in sig.split(",") if s.strip()]}
              for sid, role, _use, sig in table(idx, ["id", "role", "use when", "signals"])]
    gates = re.findall(r"\[(templates/[a-z-]+\.md)\]", text)
    return {"budget": int(m.group(1)), "profiles": profiles, "routes": routes, "always": gates}


def pick_profile(runtime, profiles):
    rt = runtime.lower()
    for signals, prof in profiles:
        if any(s != "*" and s in rt for s in signals):
            return prof
    for signals, prof in profiles:
        if "*" in signals:
            return prof
    raise ValueError("AGENTS.md: no fallback (*) profile row")


def matches(task, signal):
    return re.search(r"(?<![a-z0-9])" + re.escape(signal) + SUFFIX + r"(?![a-z0-9])", task) is not None


def route(task, routes):
    task = task.lower()
    hits = []
    for idx, r in enumerate(routes):
        n = sum(matches(task, s) for s in r["signals"])
        if n:
            hits.append((idx, n, r))
    safety = [r["id"] for idx, n, r in hits if "safety" in r["role"]]
    rest = [r["id"] for idx, n, r in sorted((h for h in hits if "safety" not in h[2]["role"]),
                                            key=lambda h: (-h[1], h[0]))]
    return (safety + rest)[:MAX_SKILLS]


def hitl_gate_check():
    """send_email must be held or denied, never executed, unless APPROVE."""
    path = os.path.join(ROOT, "skills", "human-in-the-loop", "examples", "minimal.py")
    spec = importlib.util.spec_from_file_location("hitl_minimal", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    calls = []
    real = mod.execute
    mod.execute = lambda a: calls.append(a.name) or real(a)

    def timeout(_h):
        raise TimeoutError

    act = mod.Action("send_email", "someone@example.com", irreversible=True, confidence=0.99)
    got = [mod.run(act, {}, ap).status for ap in (None, timeout, lambda h: None, lambda h: "ok")]
    executed_without_approve = list(calls)
    held = not executed_without_approve and got == ["pending_human", "denied", "denied", "denied"]
    approved = mod.run(act, {}, lambda h: "APPROVE").status == "executed" and calls == ["send_email"]
    return {"statuses": got, "executed_without_approve": executed_without_approve,
            "pass": held and approved}


def simulate(fixtures_path=FIXTURES):
    std = parse_standup()
    with open(fixtures_path, encoding="utf-8") as f:
        tasks = json.load(f)["tasks"]
    results = []
    for t in tasks:
        profile = pick_profile(t["runtime"], std["profiles"])
        skills = route(t["task"], std["routes"])
        files = BOOT_FILES + std["always"] + [profile] + [f"skills/{s}/SKILL.md" for s in skills]
        per_file = {f: tokens(f) for f in files}
        total = sum(per_file.values())
        fails = []
        if profile != t["expect_profile"]:
            fails.append(f"profile {profile} != {t['expect_profile']}")
        if sorted(skills) != sorted(t["expect_skills"]):
            fails.append(f"skills {skills} != {t['expect_skills']}")
        bad = sorted(set(skills) & set(t.get("forbid_skills", [])))
        if bad:
            fails.append(f"forbidden skills loaded: {bad}")
        if total > std["budget"]:
            fails.append(f"tokens {total} > budget {std['budget']}")
        hitl = None
        if t.get("must_trigger_hitl"):
            if "human-in-the-loop" not in skills:
                fails.append("human-in-the-loop not triggered")
            hitl = hitl_gate_check()
            if not hitl["pass"]:
                fails.append(f"HITL gate failed: {hitl}")
        results.append({"id": t["id"], "runtime": t["runtime"], "task": t["task"],
                        "profile": profile, "skills": skills, "files": per_file,
                        "tokens": total, "budget": std["budget"], "hitl": hitl,
                        "pass": not fails, "fails": fails})
    return results


def main():
    results = simulate()
    if "--json" in sys.argv:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"{'PASS' if r['pass'] else 'FAIL'}  {r['id']:20} profile={os.path.basename(r['profile'])} "
                  f"skills={r['skills']} tokens={r['tokens']}/{r['budget']}"
                  + (f" hitl={r['hitl']['statuses']}" if r["hitl"] else ""))
            for f in r["fails"]:
                print(f"      {f}")
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
