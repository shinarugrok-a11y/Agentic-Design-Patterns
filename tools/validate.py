#!/usr/bin/env python3
"""Validate the skill library and run the low-token agent simulation.

Usage: python3 tools/validate.py            check only, non-zero exit on failure
       python3 tools/validate.py --sync     first refresh token_cost_estimate in
                                            SKILL.md + manifest.json and rewrite
                                            the notebook companions, then check
Requires: pip install tiktoken

Checks structure, manifest <-> SKILL.md consistency, token caps, notebook
companions, that examples run offline, and that AGENTS.md + manifest.json +
any two same-role SKILL.md files + one references/patterns.md stays < 3000
tokens for every role pair (the Step 7 gate).

Stand-up path: STANDUP.md is linked from AGENTS.md; every profile it names
exists; its routing table lists each manifest skill id exactly once with the
manifest roles; relative links and repo paths in AGENTS.md, STANDUP.md and
models/ resolve; every deep-dive code block carries a Provenance line; the
worst-case stand-up load fits the STANDUP budget; and the fixtures in
tests/fixtures/standup_tasks.json pass (tools/standup_sim.py).

The Step 7 gate is an invariant, not a description of the current result.
Do not raise BUDGET to make a failure pass; trim AGENTS.md, manifest.json or
the heaviest cards instead (history: validation/audit/02-evidence-map.md and
validation/skill-reaudit/LOG.md).
"""
import glob
import itertools
import json
import os
import re
import subprocess
import sys

import tiktoken

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENC = tiktoken.get_encoding("cl100k_base")
ENC2 = tiktoken.get_encoding("o200k_base")
ROLES = ["planner", "executor", "critic", "memory", "safety"]
BUDGET = 3000
results = []


def check(name, ok, detail=""):
    results.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))


def tok(s):
    return len(ENC.encode(s))


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n\n(.*)$", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("["):
            v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
        elif v.isdigit():
            v = int(v)
        fm[k.strip()] = v
    return fm, m.group(2)


def write_manifest(manifest):
    """One compact record per line: keeps the index cheap to load."""
    head = {k: v for k, v in manifest.items() if k != "skills"}
    with open(os.path.join(ROOT, "manifest.json"), "w", encoding="utf-8") as f:
        f.write("{\n")
        for k, v in head.items():
            f.write(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n")
        f.write('  "skills": [\n')
        recs = manifest["skills"]
        for i, rec in enumerate(recs):
            f.write("    " + json.dumps(rec, ensure_ascii=False, separators=(",", ":"))
                    + ("," if i < len(recs) - 1 else "") + "\n")
        f.write("  ]\n}\n")


def sync(manifest):
    """Refresh token_cost_estimate (SKILL.md + manifest) and notebook companions."""
    for s in manifest["skills"]:
        p = os.path.join(ROOT, f"skills/{s['id']}/SKILL.md")
        text = read(f"skills/{s['id']}/SKILL.md")
        fm, body = parse_frontmatter(text)
        if fm is None:
            continue
        est = tok(body)
        text = re.sub(r"^token_cost_estimate: \d+$", f"token_cost_estimate: {est}", text, count=1, flags=re.M)
        s["token_cost_estimate"] = est
        open(p, "w", encoding="utf-8").write(text)
        for nb in glob.glob(os.path.join(ROOT, "chapter_notebooks", f"Chapter_{s['chapter']:02d}_*.ipynb")):
            open(nb[:-len(".ipynb")] + ".SKILL.md", "w", encoding="utf-8").write(text)
    write_manifest(manifest)
    print(f"synced token_cost_estimate and companions for {len(manifest['skills'])} skills\n")


# --- manifest -------------------------------------------------------------
manifest = json.loads(read("manifest.json"))
if "--sync" in sys.argv:
    sync(manifest)
    manifest = json.loads(read("manifest.json"))
skills = manifest["skills"]
ids = [s["id"] for s in skills]
check("manifest has 21 skills", len(skills) == 21, str(len(skills)))
check("manifest ids unique + kebab-case",
      len(set(ids)) == len(ids) and all(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i) for i in ids))
check("manifest chapters are exactly 1..21", sorted(s["chapter"] for s in skills) == list(range(1, 22)))
required = {"id", "name", "chapter", "role", "when_to_use", "when_not_to_use", "inputs", "outputs",
            "failure_modes", "chains_with", "token_cost_estimate"}
check("manifest records have all required fields", all(required <= set(s) for s in skills))
check("manifest roles valid", all(s["role"] and set(s["role"]) <= set(ROLES) for s in skills))
check("manifest chains_with resolve (2-3 each, no self)",
      all(2 <= len(s["chains_with"]) <= 3 and set(s["chains_with"]) <= set(ids) and s["id"] not in s["chains_with"]
          for s in skills))
check("manifest failure_modes 2-4 bullets", all(2 <= len(s["failure_modes"]) <= 4 for s in skills))

# --- skills ---------------------------------------------------------------
body_tok, full_tok, pat_tok = {}, {}, {}
fm_ok, est_ok, body_ok, pat_ok, missing = True, True, True, True, []
SECTIONS = ("## When to use", "## When NOT to use", "## Inputs", "## Outputs", "## Failure modes",
            "## Minimal example", "## Next skills")
for s in skills:
    d = f"skills/{s['id']}"
    for f in ("SKILL.md", "references/patterns.md", "references/deep-dive.md", "examples/minimal.py"):
        if not os.path.exists(os.path.join(ROOT, d, f)):
            missing.append(f"{d}/{f}")
    if not os.path.exists(os.path.join(ROOT, d, "SKILL.md")):
        continue
    text = read(f"{d}/SKILL.md")
    fm, body = parse_frontmatter(text)
    if fm is None or not (fm.get("name") == s["id"] and fm.get("chapter") == s["chapter"]
                          and fm.get("role") == s["role"] and fm.get("chains_with") == s["chains_with"]
                          and fm.get("token_cost_estimate") == s["token_cost_estimate"]
                          and all(h in body for h in SECTIONS)):
        fm_ok = False
    body_tok[s["id"]], full_tok[s["id"]] = tok(body), tok(text)
    est_ok &= abs(s["token_cost_estimate"] - tok(body)) <= 10
    body_ok &= tok(body) <= 400 and len(ENC2.encode(body)) <= 400
    p = os.path.join(ROOT, d, "references/patterns.md")
    pat_tok[s["id"]] = tok(read(f"{d}/references/patterns.md")) if os.path.exists(p) else 0
    pat_ok &= pat_tok[s["id"]] >= 150
check("every skill has SKILL.md, references/{patterns,deep-dive}.md, examples/minimal.py", not missing, ", ".join(missing))
check("SKILL.md frontmatter matches manifest + all body sections present", fm_ok)
check("token_cost_estimate within 10 of measured body tokens", est_ok)
check("every SKILL.md body <= 400 tokens (cl100k_base and o200k_base)", body_ok,
      f"body min {min(body_tok.values())}, max {max(body_tok.values())}, total {sum(body_tok.values())}")
check("references/patterns.md non-trivial for all skills", pat_ok,
      f"min {min(pat_tok.values())}, max {max(pat_tok.values())} tokens")
check("exactly 21 skill directories",
      len([p for p in glob.glob(os.path.join(ROOT, "skills", "*")) if os.path.isdir(p)]) == 21)

# --- examples run offline -------------------------------------------------
failed = []
for i in ids:
    p = os.path.join(ROOT, f"skills/{i}/examples/minimal.py")
    if not os.path.exists(p):
        continue
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        failed.append(f"{i}: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'exit ' + str(r.returncode)}")
check("all examples/minimal.py run offline with exit 0", not failed, "; ".join(failed))

# --- AGENTS.md ------------------------------------------------------------
agents = read("AGENTS.md")
n_lines = agents.count("\n")
check("AGENTS.md under 60 lines", n_lines < 60, f"{n_lines} lines, {tok(agents)} tokens")
check("AGENTS.md mentions every skill id", all(i in agents for i in ids))
table_ok = True
for role in ROLES:
    m = re.search(rf"^- {role}:\s*(.+)$", agents, re.M)
    listed = {x.strip() for x in m.group(1).split(",")} if m else set()
    expected = {s["id"] for s in skills if role in s["role"]}
    if listed != expected:
        table_ok = False
        print(f"      role {role}: AGENTS.md={sorted(listed)} manifest={sorted(expected)}")
check("AGENTS.md role table matches manifest roles", table_ok)
for kw in ("manifest.json", "Do not load the entire PDF", "Do not load all skills", "models/", "STANDUP.md"):
    check(f"AGENTS.md contains '{kw}'", kw in agents)

# --- stand-up path --------------------------------------------------------
sys.path.insert(0, os.path.join(ROOT, "tools"))
import standup_sim  # noqa: E402

check("STANDUP.md exists", os.path.exists(os.path.join(ROOT, "STANDUP.md")))
check("AGENTS.md links STANDUP.md in its first 6 lines",
      "](STANDUP.md)" in "\n".join(agents.splitlines()[:6]))
std = standup_sim.parse_standup()
std_profiles = sorted({p for _, p in std["profiles"]})
check("STANDUP.md has a fallback (*) profile row", any("*" in sig for sig, _ in std["profiles"]))

# --- models ---------------------------------------------------------------
for p in sorted(set(std_profiles) | {f"models/{m}.md" for m in ("fable-5-1", "grok-4-6", "muse")}):
    n = read(p).count("\n") if os.path.exists(os.path.join(ROOT, p)) else 0
    check(f"{p} exists, 30-50 lines" + (" (named in STANDUP.md)" if p in std_profiles else ""),
          30 <= n <= 50, f"{n} lines")

route_ids = [r["id"] for r in std["routes"]]
role_bad = [r["id"] for r in std["routes"] if r["id"] in ids
            and r["role"] != next(s["role"] for s in skills if s["id"] == r["id"])]
check("STANDUP routing table lists every manifest skill id exactly once, nothing else",
      sorted(route_ids) == sorted(ids), f"unknown={sorted(set(route_ids) - set(ids))} "
      f"missing={sorted(set(ids) - set(route_ids))}")
check("STANDUP routing table roles match manifest", not role_bad, ", ".join(role_bad))
check("STANDUP routing rows each have signals", all(r["signals"] for r in std["routes"]))

link_bad = []
for doc in ["AGENTS.md", "STANDUP.md"] + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "models", "*.md"))):
    text = read(doc)
    targets = re.findall(r"\]\(([^)\s#]+)", text)
    targets += [t for t in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|json|py))`", text) if "/" in t or t[0].isupper()]
    for t in targets:
        if t.startswith(("http://", "https://", "mailto:")) or "<" in t or "*" in t:
            continue
        if t.startswith(("references/", "examples/")):
            if not all(os.path.exists(os.path.join(ROOT, "skills", i, t)) for i in ids):
                link_bad.append(f"{doc}: {t} (missing in some skills/<id>/)")
            continue
        if not os.path.exists(os.path.normpath(os.path.join(ROOT, os.path.dirname(doc), t))) \
                and not os.path.exists(os.path.join(ROOT, t)):
            link_bad.append(f"{doc}: {t}")
check("links and repo paths in AGENTS.md, STANDUP.md, models/ resolve", not link_bad, "; ".join(link_bad))

prov_bad = []
for p in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "references", "deep-dive.md"))):
    lines, fence = read(os.path.relpath(p, ROOT)).split("\n"), None
    for i, ln in enumerate(lines):
        m = re.match(r"^(```|~~~)", ln)
        if fence is None and m:
            fence = m.group(1)
            para = []
            for prev in reversed(lines[max(0, i - 4):i]):
                if not prev.strip():
                    break
                para.append(prev)
            if not any(x.startswith("Provenance: ") for x in para):
                prov_bad.append(f"{os.path.relpath(p, ROOT)}:{i + 1}")
        elif fence and ln.strip() == fence:
            fence = None
check("every deep-dive code block has a Provenance: line", not prov_bad, ", ".join(prov_bad[:8]))

# --- notebook companions --------------------------------------------------
nbs = sorted(glob.glob(os.path.join(ROOT, "chapter_notebooks", "Chapter_*.ipynb")))
by_chapter = {s["chapter"]: s["id"] for s in skills}
comp_missing, comp_diff = [], []
for nb in nbs:
    ch = int(re.search(r"Chapter_(\d+)_", os.path.basename(nb)).group(1))
    comp = nb[:-len(".ipynb")] + ".SKILL.md"
    if not os.path.exists(comp):
        comp_missing.append(os.path.basename(comp))
    elif open(comp, encoding="utf-8").read() != read(f"skills/{by_chapter[ch]}/SKILL.md"):
        comp_diff.append(os.path.basename(comp))
comps = glob.glob(os.path.join(ROOT, "chapter_notebooks", "Chapter_*.SKILL.md"))
check(f"every chapter notebook ({len(nbs)}) has an identical .SKILL.md companion",
      not comp_missing and not comp_diff and len(comps) == len(nbs),
      f"companions={len(comps)} missing={comp_missing} differ={comp_diff}")

# --- originals untouched --------------------------------------------------
diff = subprocess.run(["git", "diff", "--name-status", "origin/main", "HEAD", "--"], cwd=ROOT,
                      capture_output=True, text=True).stdout
# PDF bytes and chapter notebooks stay frozen. README accuracy edits are
# allowed; they are recorded in validation/audit/04-correction-log.md.
touched = [l for l in diff.splitlines()
           if not l.startswith("A") and (".ipynb" in l or ".pdf" in l)]
check("PDF and notebooks unmodified vs origin/main", not touched, "; ".join(touched))

# --- stand-up simulation --------------------------------------------------
print(f"\n=== Stand-up simulation (cl100k_base tokens, STANDUP budget {std['budget']}) ===")
su_base = sum(standup_sim.tokens(f) for f in ("AGENTS.md", "STANDUP.md", "manifest.json"))
su_prof = max((standup_sim.tokens(p), p) for p in std_profiles)
su_top = sorted(full_tok.values(), reverse=True)[:standup_sim.MAX_SKILLS]
su_worst = su_base + su_prof[0] + sum(su_top)
print(f"worst case: base {su_base} + {su_prof[1]} {su_prof[0]} + {standup_sim.MAX_SKILLS} heaviest SKILL.md "
      f"{sum(su_top)} = {su_worst}")
check(f"stand-up worst case <= STANDUP budget {std['budget']}", su_worst <= std["budget"], f"{su_worst} tokens")
for r in standup_sim.simulate():
    print(f"  {r['id']:20} profile={os.path.basename(r['profile'])} skills={r['skills']} tokens={r['tokens']}"
          + (f" hitl={r['hitl']['statuses']}" if r["hitl"] else ""))
    check(f"fixture {r['id']}", r["pass"], "; ".join(r["fails"]))

# --- Step 7: low-token agent simulation -----------------------------------
print(f"\n=== Low-token agent simulation (cl100k_base tokens, budget {BUDGET}) ===")
base = tok(agents) + tok(read("manifest.json"))
print(f"AGENTS.md      {tok(agents):>5}\nmanifest.json  {tok(read('manifest.json')):>5}\nbase           {base:>5}")
rows = []
for role in ROLES:
    members = [s["id"] for s in skills if role in s["role"]]
    for a, b in itertools.combinations(members, 2):
        for ref in (a, b):
            rows.append((base + full_tok[a] + full_tok[b] + pat_tok[ref], role, a, b, ref))
rows.sort()
best, worst = rows[0], rows[-1]
print(f"combos (same-role pair + one patterns.md): {len(rows)}; under budget: {sum(r[0] < BUDGET for r in rows)}")
print(f"  best  {best[0]}: {best[1]} {best[2]}+{best[3]} ref={best[4]}")
print(f"  worst {worst[0]}: {worst[1]} {worst[2]}+{worst[3]} ref={worst[4]}")
ex = base + full_tok["prompt-chaining"] + full_tok["tool-use"] + pat_tok["tool-use"]
print(f"executor walk-through: {tok(agents)} + {tok(read('manifest.json'))} + {full_tok['prompt-chaining']} "
      f"+ {full_tok['tool-use']} + {pat_tok['tool-use']} = {ex}")
check(f"simulation: executor walk-through < {BUDGET}", ex < BUDGET, f"{ex} tokens")
check(f"simulation: every role pair + one patterns.md < {BUDGET}", worst[0] < BUDGET, f"worst {worst[0]} tokens")

print(f"\n{'id':30}{'body':>6}{'SKILL.md':>10}{'patterns':>10}")
for s in skills:
    print(f"{s['id']:30}{body_tok[s['id']]:>6}{full_tok[s['id']]:>10}{pat_tok[s['id']]:>10}")
fails = sum(1 for _, ok in results if not ok)
print(f"\n{len(results) - fails} passed, {fails} failed")
sys.exit(1 if fails else 0)
