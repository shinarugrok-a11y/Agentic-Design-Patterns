#!/usr/bin/env python3
"""Expected-PASS / FAIL / BLOCKED fixtures for tools/validate.py.

Each case in tests/fixtures/validator_cases.json is a mutation spec. The runner
copies the repository into a temp directory without .git, applies the
mutations, runs that copy's validator with --no-fixtures --report, and checks
the exit code (0 PASS, 1 FAIL, 2 BLOCKED) and the named check statuses.
The PDF, the ground-truth text and the notebooks are symlinked rather than
copied; a mutation on a symlinked file replaces the link with a real copy
first, so the originals are never written. A case with "twice" runs the
validator again and requires an unchanged tree and identical statuses;
"expect_unchanged" requires that the run wrote nothing.

Usage: python3 tools/validator_fixtures.py     (tools/validate.py also runs it)
"""
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "tests", "fixtures", "validator_cases.json")
EXIT = {"PASS": 0, "FAIL": 1, "BLOCKED": 2}
SKIP_DIRS = {".git", "__pycache__"}


def big(rel):
    return rel.endswith((".pdf", ".ipynb")) or rel == "ground-truth/agentic_design_patterns.txt"


def make_copy(dst):
    for d, dirs, files in os.walk(ROOT):
        rel_d = os.path.relpath(d, ROOT)
        keep = []
        for x in dirs:
            src = os.path.join(d, x)
            if x in SKIP_DIRS:
                continue
            if os.path.islink(src):
                os.symlink(os.readlink(src), os.path.join(dst, rel_d, x))
            else:
                keep.append(x)
                os.makedirs(os.path.join(dst, rel_d, x), exist_ok=True)
        dirs[:] = keep
        for f in files:
            src, rel = os.path.join(d, f), os.path.normpath(os.path.join(rel_d, f))
            out = os.path.join(dst, rel)
            if os.path.islink(src):
                os.symlink(os.readlink(src), out)
            elif big(rel):
                os.symlink(src, out)
            else:
                shutil.copy2(src, out)


def snapshot(root):
    snap = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            p = os.path.join(d, f)
            with open(p, "rb") as fh:
                snap[os.path.relpath(p, root)] = hashlib.sha256(fh.read()).hexdigest()
    return snap


def mutate(root, m):
    path = os.path.join(root, m["path"])
    if os.path.islink(path):
        data = open(path, "rb").read()
        os.unlink(path)
        if m["op"] != "delete":
            open(path, "wb").write(data)
    if m["op"] == "delete":
        if os.path.lexists(path):
            os.remove(path)
        return
    if m["op"] == "write":
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(m["content"])
        return
    text = open(path, encoding="utf-8").read()
    if m["op"] == "append":
        text += m["content"]
    elif m["op"] == "prepend":
        text = m["content"] + text
    elif m["op"] == "replace":
        if text.count(m["old"]) != 1:
            raise ValueError(f"fixture mutation: {m['path']} has {text.count(m['old'])} copies of {m['old'][:40]!r}")
        text = text.replace(m["old"], m["new"])
    else:
        raise ValueError(f"unknown op {m['op']}")
    open(path, "w", encoding="utf-8").write(text)


def run_validator(root, report, case):
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env.update(case.get("env", {}))
    if case.get("hide_tiktoken"):
        shadow = os.path.join(os.path.dirname(root), "shadow")
        os.makedirs(shadow, exist_ok=True)
        open(os.path.join(shadow, "tiktoken.py"), "w").write('raise ImportError("tiktoken hidden by fixture")\n')
        env["PYTHONPATH"] = shadow
    cmd = [sys.executable, os.path.join(root, "tools", "validate.py"), "--no-fixtures", "--report", report]
    r = subprocess.run(cmd + case.get("args", []), capture_output=True, text=True, timeout=600, env=env, cwd=root)
    statuses = {}
    if os.path.exists(report):
        statuses = {x["check"]: x["status"] for x in json.load(open(report))["results"]}
        os.remove(report)
    return r, statuses


def run_case(case):
    tmp = tempfile.mkdtemp(prefix="adp-fixture-")
    try:
        root = os.path.join(tmp, "repo")
        os.makedirs(root)
        make_copy(root)
        for m in case.get("mutations", []):
            mutate(root, m)
        before = snapshot(root)
        r, statuses = run_validator(root, os.path.join(tmp, "report.json"), case)
        want = EXIT[case["expect"]]
        problems = [] if r.returncode == want else [f"exit {r.returncode}, want {want}"]
        for name_part, status in case.get("expect_status", {}).items():
            hits = {k: v for k, v in statuses.items() if name_part in k}
            if not hits:
                problems.append(f"no check matching {name_part!r}")
            elif status not in hits.values():
                problems.append(f"{name_part!r} is {sorted(set(hits.values()))}, want {status}")
        for text in case.get("expect_output", []):
            if text not in r.stdout + r.stderr:
                problems.append(f"output lacks {text!r}")
        if case.get("expect_unchanged") and snapshot(root) != before:
            problems.append("validator wrote to the tree")
        if os.path.lexists(os.path.join(tmp, "evil")) or os.path.lexists(os.path.join(os.path.dirname(tmp), "evil")):
            problems.append("a file was written outside the repo copy")
        if "Traceback" in r.stderr:
            problems.append("validator crashed: " + r.stderr.strip().splitlines()[-1][:120])
        if case.get("twice"):
            r2, statuses2 = run_validator(root, os.path.join(tmp, "report.json"), case)
            if snapshot(root) != before:
                problems.append("tree changed across runs")
            if r2.returncode != r.returncode or statuses2 != statuses:
                problems.append("second run differs")
        counts = {k: list(statuses.values()).count(k) for k in EXIT}
        evidence = (f"exit {r.returncode}; {counts['PASS']} PASS {counts['FAIL']} FAIL {counts['BLOCKED']} BLOCKED"
                    + ("; twice: tree and statuses unchanged" if case.get("twice") and not problems else ""))
        return {"id": case["id"], "expect": case["expect"], "ok": not problems,
                "evidence": "; ".join(problems) if problems else evidence}
    except Exception as e:  # a fixture that cannot run is BLOCKED, not passed
        return {"id": case["id"], "expect": case["expect"], "ok": None,
                "evidence": f"fixture could not run: {type(e).__name__}: {e}"}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_all(path=CASES):
    cases = json.load(open(path, encoding="utf-8"))["cases"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(6, os.cpu_count() or 2)) as pool:
        return list(pool.map(run_case, cases))


if __name__ == "__main__":
    out = run_all()
    for c in out:
        print(f"{'PASS' if c['ok'] else 'BLOCKED' if c['ok'] is None else 'FAIL':7}  {c['id']:28} "
              f"expect {c['expect']:7} {c['evidence']}")
    sys.exit(0 if all(c["ok"] for c in out) else 1)
