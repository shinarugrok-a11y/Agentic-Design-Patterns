#!/usr/bin/env python3
"""Validate the skill library: PASS / FAIL / BLOCKED per check, with evidence.

Usage: python3 tools/validate.py              all checks + validator fixtures (one command)
       python3 tools/validate.py --sync       first refresh token_cost_estimate in SKILL.md +
                                              manifest.json, the notebook companions, both
                                              INDEX.md files and .agents/skills, then check
       options: --no-fixtures, --report PATH (JSON results)
Exit: 0 all PASS, 1 any FAIL, 2 no FAIL but something BLOCKED.
Requires: Python 3.10+, pip install tiktoken. Offline: network calls are refused
in-process and in every example (tools/offline.py). No git needed.

Acceptance rule: unknown = BLOCKED, never PASS. A missing tiktoken, an
unreadable file, a missing example, an example timeout (VALIDATE_EXAMPLE_TIMEOUT,
default 60 s), missing hash pins or a validator error each give BLOCKED for the
affected checks and a nonzero exit, not a crash and not a pass. A check-only run
must leave the tree byte-identical (checked at the end).

Checks: manifest schema (21 pattern skills, chapters 1..21; operational skills
have chapter null); SKILL.md frontmatter and sections; token caps; every
examples/minimal.py runs offline; AGENTS.md (under 60 lines, role table, boot
steps each with a Done: check, profile table); skills/INDEX.md and
ground-truth/INDEX.md equal their renders; GEMINI.md pointer; no CLAUDE.md;
.agents/skills mirrors; templates and .env.example; links; Provenance lines;
notebook companions; the PDF and notebooks match validation/frozen-sha256.txt;
the stand-up worst case fits the AGENTS.md budget; the routing fixtures in
tests/fixtures/standup_tasks.json (a deterministic routing-table test, not a
behavioural test of a real agent); the Step 7 gate; and the mutation fixtures in
tests/fixtures/validator_cases.json (tools/validator_fixtures.py).

Step 7 gate: the boot base (AGENTS.md + skills/INDEX.md + the templates/*.md
that AGENTS.md links, i.e. the gates) + any two same-role SKILL.md files + one
references/patterns.md stays < 3000 cl100k tokens for every role pair. It was
AGENTS.md + manifest.json before the slim index existed. The gate is an
invariant: do not raise BUDGET to make a failure pass; trim instead (history:
validation/audit/02-evidence-map.md, validation/skill-reaudit/LOG.md).
"""
import glob
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys

try:
    import tiktoken
except ImportError:
    tiktoken = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import offline  # noqa: E402

ENC = tiktoken.get_encoding("cl100k_base") if tiktoken else None
ENC2 = tiktoken.get_encoding("o200k_base") if tiktoken else None
ROLES = ["planner", "executor", "critic", "memory", "safety"]
BUDGET = 3000
FROZEN_PINS = "validation/frozen-sha256.txt"
EXAMPLE_TIMEOUT = float(os.environ.get("VALIDATE_EXAMPLE_TIMEOUT", "60"))
results = []


class Blocked(Exception):
    """A check could not run, so its result is unknown. Unknown is BLOCKED, never PASS."""


def check(name, ok, detail=""):
    """ok: True = PASS, False = FAIL, None = BLOCKED. detail is the evidence."""
    status = "BLOCKED" if ok is None else "PASS" if ok else "FAIL"
    results.append({"check": name, "status": status, "evidence": detail})
    print(f"{status:7}  {name}" + (f"  -- {detail}" if detail else ""))


def section(title, fn):
    print(f"\n--- {title}")
    try:
        fn()
    except Blocked as e:
        check(f"{title}: remaining checks", None, str(e))
    except KeyError as e:
        why = (f"depends on an earlier section that did not finish (no {e})" if e.args and e.args[0] not in S
               else f"validator error KeyError: {e}")
        check(f"{title}: remaining checks", None, why)
    except Exception as e:  # a validator crash is an unknown result, not a pass
        check(f"{title}: remaining checks", None, f"validator error {type(e).__name__}: {e}")


def tok(s):
    if ENC is None:
        raise Blocked("tiktoken not installed (pip install tiktoken); token counts unknown")
    return len(ENC.encode(s))


def tok2(s):
    if ENC2 is None:
        raise Blocked("tiktoken not installed (pip install tiktoken); token counts unknown")
    return len(ENC2.encode(s))


def exists(p):
    return os.path.exists(os.path.join(ROOT, p))


def read(p):
    if not os.path.isfile(os.path.join(ROOT, p)):
        raise Blocked(f"cannot read {p}: file missing")
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def tree_snapshot():
    """sha256 of every file (or symlink target) outside .git and __pycache__."""
    snap = {}
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in (".git", "__pycache__")
                         and not os.path.islink(os.path.join(d, x)))
        for name in files + [x for x in os.listdir(d) if os.path.islink(os.path.join(d, x))
                             and os.path.isdir(os.path.join(d, x))]:
            p = os.path.join(d, name)
            rel = os.path.relpath(p, ROOT)
            if os.path.islink(p):
                snap[rel] = "link:" + os.readlink(p)
            else:
                with open(p, "rb") as f:
                    snap[rel] = hashlib.sha256(f.read()).hexdigest()
    return snap


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
        elif v == "null":
            v = None
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


INDEX_PATH = "skills/INDEX.md"
ID_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
GT_INDEX_PATH = "ground-truth/INDEX.md"
MIRROR_DIR = ".agents/skills"


def render_index(manifest):
    """The slim index bots read at boot (manifest.json stays the full record for tools)."""
    out = ["# Skill index", "",
           "Generated from `manifest.json` by `python3 tools/validate.py --sync`; do not edit.", "",
           "Pick rule: lowercase the task; a signal matches as a whole word or phrase (+ s, es, d, ed, ing). "
           "Safety rows that match come first, then others by most matches, then table order. Load at most 3 "
           "`skills/<id>/SKILL.md`, none if nothing matches.", "",
           "| id | role | use when | signals |", "|---|---|---|---|"]
    for s in manifest["skills"]:
        out.append(f"| {s['id']} | {', '.join(s['role'])} | {s['when_to_use']} | {', '.join(s['signals'])} |")
    return "\n".join(out) + "\n"


def render_gt_index():
    """Chapter, appendix and back-matter line ranges in the ground-truth text (1-based, inclusive)."""
    lines = read("ground-truth/agentic_design_patterns.txt").split("\n")
    names = {s["chapter"]: s["name"] for s in json.loads(read("manifest.json"))["skills"] if s.get("chapter")}
    parts = []
    for i, l in enumerate(lines):
        m = re.match(r"^\f?Chapter (\d+): ", l)
        if m and int(m.group(1)) == len([p for p in parts if p[0].startswith("Chapter")]) + 1:
            parts.append((f"Chapter {m.group(1)}", i, names.get(int(m.group(1)), l.strip())))
            continue
        m = re.match(r"^\f(Appendix ([A-G]))[: -]+(.+)$", l)
        if m:
            parts.append((m.group(1), i, m.group(3).strip()))
        elif l in ("\fGlossary", "\fIndex of Terms"):
            parts.append(("Back matter", i, l.lstrip("\f")))
    out = ["# Ground-truth line index", "",
           "Generated by `python3 tools/validate.py --sync` from `agentic_design_patterns.txt`; do not edit.",
           "Read only the range you need, e.g. `sed -n '7539,7807p' ground-truth/agentic_design_patterns.txt`.",
           "Line numbers are as `grep -n` and `sed -n` print them; the file has no final newline, so",
           "`wc -l` reports one fewer. Appendix titles are the first heading line as printed.", "",
           "| part | title | lines |", "|---|---|---|"]
    for k, (label, s0, title) in enumerate(parts):
        e = parts[k + 1][1] if k + 1 < len(parts) else len(lines) - (lines[-1] == "")
        out.append(f"| {label} | {title} | {s0 + 1}-{e} |")
    return "\n".join(out) + "\n"


def mirror_target(i):
    return os.path.join("..", "..", "skills", i)


def sync(manifest):
    """Refresh token_cost_estimate (SKILL.md + manifest), notebook companions, the
    generated indexes and the .agents/skills mirror symlinks.

    Ids and chapters become file paths, so they are validated before anything is written."""
    bad = [repr(s.get("id")) for s in manifest["skills"]
           if not (isinstance(s.get("id"), str) and ID_RE.fullmatch(s["id"])
                   and ((type(s.get("chapter")) is int and 1 <= s["chapter"] <= 99)
                        or (s.get("chapter") is None and s.get("kind") == "operational")))]
    if bad:
        sys.exit(f"sync refused: unsafe manifest id/chapter {', '.join(bad)}; nothing written")
    if ENC is None:
        print("BLOCKED  sync needs tiktoken (pip install tiktoken); nothing written")
        sys.exit(2)
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
        for nb in (glob.glob(os.path.join(ROOT, "chapter_notebooks", f"Chapter_{s['chapter']:02d}_*.ipynb"))
                   if s["chapter"] is not None else []):
            open(nb[:-len(".ipynb")] + ".SKILL.md", "w", encoding="utf-8").write(text)
    write_manifest(manifest)
    open(os.path.join(ROOT, INDEX_PATH), "w", encoding="utf-8").write(render_index(manifest))
    open(os.path.join(ROOT, GT_INDEX_PATH), "w", encoding="utf-8").write(render_gt_index())
    os.makedirs(os.path.join(ROOT, MIRROR_DIR), exist_ok=True)
    for s in manifest["skills"]:
        link = os.path.join(ROOT, MIRROR_DIR, s["id"])
        if os.path.islink(link) and os.readlink(link) == mirror_target(s["id"]):
            continue
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(mirror_target(s["id"]), link)
    print(f"synced token_cost_estimate, companions, indexes and mirrors for {len(manifest['skills'])} skills\n")


# --- run -------------------------------------------------------------------
offline.block_network()
S = {}  # state shared between sections


def sec_manifest():
    try:
        manifest = json.loads(read("manifest.json"))
    except json.JSONDecodeError as e:
        raise Blocked(f"manifest.json is not valid JSON: line {e.lineno}")
    skills = manifest["skills"]
    S.update(manifest=manifest, skills=skills, ids=[s.get("id") for s in skills])
    ids = S["ids"]
    S["patterns"] = patterns = [s for s in skills if s.get("kind") == "pattern"]
    operational = [s for s in skills if s.get("kind") == "operational"]
    check("manifest kinds are pattern or operational", len(patterns) + len(operational) == len(skills),
          f"{len(patterns)} pattern, {len(operational)} operational, {len(skills)} total")
    check("manifest has 21 pattern skills (one per chapter)", len(patterns) == 21, str(len(patterns)))
    check("operational skills have chapter null", all(s.get("chapter") is None for s in operational),
          ", ".join(s["id"] for s in operational))
    check("manifest ids unique + kebab-case",
          len(set(ids)) == len(ids) and all(isinstance(i, str) and ID_RE.fullmatch(i) for i in ids),
          f"{len(ids)} ids")
    chapters = sorted(s["chapter"] for s in patterns if type(s.get("chapter")) is int)
    check("pattern skill chapters are exactly 1..21", chapters == list(range(1, 22)), f"{chapters[:3]}..{chapters[-3:]}")
    required = {"id", "name", "chapter", "role", "when_to_use", "when_not_to_use", "inputs", "outputs",
                "failure_modes", "chains_with", "token_cost_estimate", "kind", "signals"}
    lacking = [f"{s.get('id')}: {sorted(required - set(s))}" for s in skills if not required <= set(s)]
    check("manifest records have all required fields", not lacking, "; ".join(lacking))
    if lacking:
        raise Blocked("later manifest checks need every required field")
    check("manifest roles valid", all(s["role"] and set(s["role"]) <= set(ROLES) for s in skills))
    check("manifest chains_with resolve (2-3 each, no self)",
          all(2 <= len(s["chains_with"]) <= 3 and set(s["chains_with"]) <= set(ids)
              and s["id"] not in s["chains_with"] for s in skills))
    check("manifest failure_modes 2-4 bullets", all(2 <= len(s["failure_modes"]) <= 4 for s in skills))


SECTIONS = ("## When to use", "## When NOT to use", "## Inputs", "## Outputs", "## Failure modes",
            "## Minimal example", "## Next skills")


def sec_skill_structure():
    skills, ids = S["skills"], S["ids"]
    missing, fm_bad = [], []
    for s in skills:
        d = f"skills/{s['id']}"
        missing += [f"{d}/{f}" for f in ("SKILL.md", "references/patterns.md", "references/deep-dive.md",
                                         "examples/minimal.py") if not exists(f"{d}/{f}")]
        if not exists(f"{d}/SKILL.md"):
            continue
        fm, body = parse_frontmatter(read(f"{d}/SKILL.md"))
        if fm is None or not (fm.get("name") == s["id"] and fm.get("chapter") == s["chapter"]
                              and fm.get("kind", "pattern") == s["kind"]
                              and fm.get("role") == s["role"] and fm.get("chains_with") == s["chains_with"]
                              and fm.get("token_cost_estimate") == s["token_cost_estimate"]
                              and all(h in body for h in SECTIONS)):
            fm_bad.append(s["id"])
    check("every skill has SKILL.md, references/{patterns,deep-dive}.md, examples/minimal.py",
          not missing, ", ".join(missing) or f"{len(skills)} skills x 4 files")
    check("SKILL.md frontmatter matches manifest + all body sections present", not fm_bad, ", ".join(fm_bad))
    dirs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "skills", "*")) if os.path.isdir(p))
    check("skill directories are exactly the manifest ids", dirs == sorted(ids),
          f"extra={sorted(set(dirs) - set(ids))} missing={sorted(set(ids) - set(dirs))}")


def sec_skill_tokens():
    body_tok, full_tok, pat_tok, est_bad, cap_bad, pat_bad = {}, {}, {}, [], [], []
    for s in S["skills"]:
        d = f"skills/{s['id']}"
        if not exists(f"{d}/SKILL.md") or not exists(f"{d}/references/patterns.md"):
            raise Blocked(f"{d}: SKILL.md or references/patterns.md missing; token counts unknown")
        text = read(f"{d}/SKILL.md")
        _, body = parse_frontmatter(text)
        body_tok[s["id"]], full_tok[s["id"]] = tok(body), tok(text)
        pat_tok[s["id"]] = tok(read(f"{d}/references/patterns.md"))
        if abs(s["token_cost_estimate"] - body_tok[s["id"]]) > 10:
            est_bad.append(f"{s['id']} {s['token_cost_estimate']} vs {body_tok[s['id']]}")
        if body_tok[s["id"]] > 400 or tok2(body) > 400:
            cap_bad.append(s["id"])
        if pat_tok[s["id"]] < 150:
            pat_bad.append(s["id"])
    S.update(body_tok=body_tok, full_tok=full_tok, pat_tok=pat_tok)
    check("token_cost_estimate within 10 of measured body tokens", not est_bad, "; ".join(est_bad))
    check("every SKILL.md body <= 400 tokens (cl100k_base and o200k_base)", not cap_bad,
          ", ".join(cap_bad) or f"body min {min(body_tok.values())}, max {max(body_tok.values())}, "
          f"total {sum(body_tok.values())}")
    check("references/patterns.md non-trivial for all skills", not pat_bad,
          ", ".join(pat_bad) or f"min {min(pat_tok.values())}, max {max(pat_tok.values())} tokens")


def sec_examples():
    runner = os.path.join(ROOT, "tools", "offline.py")
    for i in S["ids"]:
        rel = f"skills/{i}/examples/minimal.py"
        if not exists(rel):
            check(f"example {i} runs offline, exit 0", None, f"{rel} missing; cannot run")
            continue
        try:
            r = subprocess.run([sys.executable, runner, os.path.join(ROOT, rel)], capture_output=True,
                               text=True, timeout=EXAMPLE_TIMEOUT, cwd=ROOT)
        except subprocess.TimeoutExpired:
            check(f"example {i} runs offline, exit 0", None, f"timed out after {EXAMPLE_TIMEOUT:g}s")
            continue
        last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""
        check(f"example {i} runs offline, exit 0", r.returncode == 0,
              f"exit {r.returncode}" + (f": {last[:160]}" if r.returncode else ""))


def sec_agents():
    agents = S["agents"] = read("AGENTS.md")
    skills, ids = S["skills"], S["ids"]
    n_lines = agents.count("\n")
    check("AGENTS.md under 60 lines", n_lines < 60, f"{n_lines} lines")
    check("AGENTS.md mentions every skill id", all(i in agents for i in ids),
          ", ".join(i for i in ids if i not in agents))
    bad = []
    for role in ROLES:
        m = re.search(rf"^- {role}:\s*(.+)$", agents, re.M)
        listed = {x.strip() for x in m.group(1).split(",")} if m else set()
        expected = {s["id"] for s in skills if role in s["role"]}
        if listed != expected:
            bad.append(f"{role}: +{sorted(listed - expected)} -{sorted(expected - listed)}")
    check("AGENTS.md role table matches manifest roles", not bad, "; ".join(bad))
    for kw in ("skills/INDEX.md", "Do not load the entire PDF", "Do not load all skills", "models/", "GEMINI.md"):
        check(f"AGENTS.md contains '{kw}'", kw in agents)
    steps = re.split(r"^(?=\d+\. \*\*)", agents.split("## Boot", 1)[-1].split("\n## ", 1)[0], flags=re.M)[1:]
    nums = [int(st.split(".", 1)[0]) for st in steps]
    no_done = [n for n, st in zip(nums, steps) if "Done:" not in st]
    check("AGENTS.md has >= 5 ordered boot steps, each with a Done: check",
          len(steps) >= 5 and not no_done and nums == list(range(1, len(steps) + 1)),
          f"{len(steps)} steps; numbering {nums}; without Done: {no_done}")


def sec_entry():
    import standup_sim
    S["std"] = std = standup_sim.parse_standup()
    S["std_profiles"] = sorted({p for _, p in std["profiles"]})
    ids, skills = S["ids"], S["skills"]
    check("AGENTS.md profile table has a fallback (*) row", any("*" in sig for sig, _ in std["profiles"]))
    check(f"{INDEX_PATH} matches render from manifest.json (run --sync)",
          exists(INDEX_PATH) and read(INDEX_PATH) == render_index(S["manifest"]))
    check(f"{GT_INDEX_PATH} matches render from the ground-truth text (run --sync)",
          exists(GT_INDEX_PATH) and read(GT_INDEX_PATH) == render_gt_index())
    gemini = read("GEMINI.md") if exists("GEMINI.md") else ""
    check("GEMINI.md is a one-line pointer to AGENTS.md", gemini.count("\n") == 1 and "](AGENTS.md)" in gemini)
    check("no CLAUDE.md (Claude Code then falls back to AGENTS.md)", not os.path.lexists(os.path.join(ROOT, "CLAUDE.md")))
    mdir = os.path.join(ROOT, MIRROR_DIR)
    mirror = sorted(os.listdir(mdir)) if os.path.isdir(mdir) else []
    mirror_bad = [i for i in ids if not (os.path.islink(os.path.join(mdir, i))
                                         and os.readlink(os.path.join(mdir, i)) == mirror_target(i)
                                         and os.path.isfile(os.path.join(mdir, i, "SKILL.md")))]
    check(f"{MIRROR_DIR}/<id> symlinks to skills/<id> for every id, nothing else",
          not mirror_bad and mirror == sorted(ids), f"bad={mirror_bad} extra={sorted(set(mirror) - set(ids))}")
    check("README.md first 12 lines point agents at AGENTS.md",
          "AGENTS.md" in "\n".join(read("README.md").splitlines()[:12]))
    for p in sorted(set(S["std_profiles"]) | {f"models/{m}.md" for m in ("fable-5-1", "grok-4-6", "muse")}):
        n = read(p).count("\n") if exists(p) else 0
        check(f"{p} exists, 30-50 lines" + (" (named in AGENTS.md)" if p in S["std_profiles"] else ""),
              30 <= n <= 50, f"{n} lines")
    route_ids = [r["id"] for r in std["routes"]]
    role_bad = [r["id"] for r in std["routes"] if r["id"] in ids
                and r["role"] != next(s["role"] for s in skills if s["id"] == r["id"])]
    check(f"{INDEX_PATH} lists every manifest skill id exactly once, nothing else",
          sorted(route_ids) == sorted(ids), f"unknown={sorted(set(route_ids) - set(ids))} "
          f"missing={sorted(set(ids) - set(route_ids))}")
    check(f"{INDEX_PATH} roles match manifest", not role_bad, ", ".join(role_bad))
    check(f"{INDEX_PATH} rows each have signals", all(r["signals"] for r in std["routes"]))


TEMPLATES = ["templates/gates.md", "templates/connectors.md", "templates/profile.md",
             "templates/memory-seed.md", "templates/routines.md"]
MUST_NOT_EXIST = {"CLAUDE.md"}


def sec_templates():
    missing = [t for t in TEMPLATES if not exists(t)]
    check("operational templates exist and are labelled DERIVED/operational",
          not missing and all("DERIVED/operational" in read(t) for t in TEMPLATES), ", ".join(missing))
    check("AGENTS.md boot path links templates/gates.md", "templates/gates.md" in S["std"]["always"])
    gates = read("templates/gates.md") if exists("templates/gates.md") else ""
    check("gates template has G1-G7 and ship = NO default",
          all(f"| G{k} |" in gates for k in range(1, 8)) and "`ship = NO`" in gates)
    env = [l for l in read(".env.example").splitlines() if l.strip() and not l.startswith("#")] \
        if exists(".env.example") else None
    bad_env = [] if env is None else [l.split("=", 1)[0] for l in env if not re.fullmatch(r"[A-Z][A-Z0-9_]*=", l)]
    check(".env.example exists with empty placeholders only", env is not None and not bad_env,
          "missing" if env is None else (f"non-empty or malformed: {bad_env}" if bad_env else f"{len(env)} names"))
    models = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "models", "*.md")))
    no_ptr = [m for m in models if "templates/gates.md" not in read(m)]
    check("every models/*.md points its gate rules at templates/gates.md", not no_ptr, ", ".join(no_ptr))


def sec_links():
    ids = S["ids"]
    link_bad = []
    docs = ["AGENTS.md", "GEMINI.md", INDEX_PATH] + sorted(set(S["std"]["always"]) | set(TEMPLATES)) + sorted(
        os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "models", "*.md")))
    for doc in docs:
        if not exists(doc):
            link_bad.append(f"{doc} (missing)")
            continue
        text = read(doc)
        targets = re.findall(r"\]\(([^)\s#]+)", text)
        targets += [t for t in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|json|py))`", text) if "/" in t or t[0].isupper()]
        for t in targets:
            if t.startswith(("http://", "https://", "mailto:")) or "<" in t or "*" in t or t in MUST_NOT_EXIST:
                continue
            if t.startswith(("references/", "examples/")):
                if not all(exists(f"skills/{i}/{t}") for i in ids):
                    link_bad.append(f"{doc}: {t} (missing in some skills/<id>/)")
                continue
            if not os.path.exists(os.path.normpath(os.path.join(ROOT, os.path.dirname(doc), t))) and not exists(t):
                link_bad.append(f"{doc}: {t}")
    check("links and repo paths in AGENTS.md, GEMINI.md, the index, templates and models/ resolve",
          not link_bad, "; ".join(link_bad) or f"{len(docs)} docs")
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


def sec_companions():
    nbs = sorted(glob.glob(os.path.join(ROOT, "chapter_notebooks", "Chapter_*.ipynb")))
    by_chapter = {s["chapter"]: s["id"] for s in S["patterns"]}
    comp_missing, comp_diff = [], []
    for nb in nbs:
        ch = int(re.search(r"Chapter_(\d+)_", os.path.basename(nb)).group(1))
        comp = os.path.relpath(nb[:-len(".ipynb")] + ".SKILL.md", ROOT)
        if not exists(comp):
            comp_missing.append(os.path.basename(comp))
        elif read(comp) != read(f"skills/{by_chapter[ch]}/SKILL.md"):
            comp_diff.append(os.path.basename(comp))
    comps = glob.glob(os.path.join(ROOT, "chapter_notebooks", "Chapter_*.SKILL.md"))
    check(f"every chapter notebook ({len(nbs)}) has an identical .SKILL.md companion",
          not comp_missing and not comp_diff and len(comps) == len(nbs),
          f"companions={len(comps)} missing={comp_missing} differ={comp_diff}")


def sec_frozen():
    """PDF bytes and chapter notebooks stay frozen; checked against pinned hashes, so no git is needed."""
    if not exists(FROZEN_PINS):
        check("PDF and notebooks match pinned SHA-256", None, f"{FROZEN_PINS} missing; cannot verify")
        return
    pins = {}
    for line in read(FROZEN_PINS).splitlines():
        if line.strip() and not line.startswith("#"):
            h, path = line.split(None, 1)
            pins[path.strip()] = h
    present = {os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "chapter_notebooks", "*.ipynb"))
               + glob.glob(os.path.join(ROOT, "*.pdf"))}
    changed, gone = [], []
    for path, h in sorted(pins.items()):
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full):
            gone.append(path)
            continue
        with open(full, "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != h:
                changed.append(path)
    unpinned = sorted(present - set(pins))
    check("PDF and notebooks match pinned SHA-256", not changed and not gone and not unpinned,
          f"{len(pins)} pinned; changed={changed} missing={gone} unpinned={unpinned}")


def sec_standup():
    import standup_sim
    std, full_tok = S["std"], S["full_tok"]
    files = standup_sim.BOOT_FILES + std["always"]
    base = sum(standup_sim.tokens(f) for f in files)
    prof = max((standup_sim.tokens(p), p) for p in S["std_profiles"])
    top = sorted(full_tok.values(), reverse=True)[:standup_sim.MAX_SKILLS]
    worst = base + prof[0] + sum(top)
    print("boot files: " + ", ".join(f"{f} {standup_sim.tokens(f)}" for f in files))
    print(f"worst case: base {base} + {prof[1]} {prof[0]} + {standup_sim.MAX_SKILLS} heaviest SKILL.md "
          f"{sum(top)} = {worst} (headroom {std['budget'] - worst})")
    check(f"stand-up worst case <= budget {std['budget']}", worst <= std["budget"], f"{worst} tokens")
    for r in standup_sim.simulate():
        check(f"routing fixture {r['id']}", r["pass"], "; ".join(r["fails"]) or
              f"profile={os.path.basename(r['profile'])} skills={r['skills']} tokens={r['tokens']}"
              + (f" hitl={r['hitl']['statuses']}" if r["hitl"] else ""))


def sec_step7():
    std, full_tok, pat_tok, skills = S["std"], S["full_tok"], S["pat_tok"], S["skills"]
    a_tok, i_tok = tok(S["agents"]), tok(read(INDEX_PATH))
    g_tok = sum(tok(read(f)) for f in std["always"])
    base = a_tok + i_tok + g_tok
    print(f"AGENTS.md {a_tok} + skills/INDEX.md {i_tok} + {' + '.join(std['always']) or 'no templates'} {g_tok}"
          f" = base {base} (manifest.json {tok(read('manifest.json'))} is for tools, not on the boot path)")
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
    print(f"  worst {worst[0]}: {worst[1]} {worst[2]}+{worst[3]} ref={worst[4]} (headroom {BUDGET - worst[0]})")
    ex = base + full_tok["prompt-chaining"] + full_tok["tool-use"] + pat_tok["tool-use"]
    check(f"simulation: executor walk-through < {BUDGET}", ex < BUDGET,
          f"{base} + {full_tok['prompt-chaining']} + {full_tok['tool-use']} + {pat_tok['tool-use']} = {ex}")
    check(f"simulation: every role pair + one patterns.md < {BUDGET}", worst[0] < BUDGET,
          f"worst {worst[0]} ({worst[1]} {worst[2]}+{worst[3]} ref={worst[4]}), headroom {BUDGET - worst[0]}")
    print(f"\n{'id':30}{'body':>6}{'SKILL.md':>10}{'patterns':>10}")
    for s in skills:
        print(f"{s['id']:30}{S['body_tok'][s['id']]:>6}{full_tok[s['id']]:>10}{pat_tok[s['id']]:>10}")


def sec_fixtures():
    import validator_fixtures
    for case in validator_fixtures.run_all():
        check(f"validator fixture {case['id']} (expect {case['expect']})", case["ok"], case["evidence"])


def main():
    if "--sync" in sys.argv:
        try:
            sync(json.loads(read("manifest.json")))
        except Blocked as e:
            print(f"BLOCKED  sync: {e}; nothing more written")
            sys.exit(2)
    before = tree_snapshot()
    section("manifest", sec_manifest)
    section("skill structure", sec_skill_structure)
    section("skill tokens", sec_skill_tokens)
    section("examples (network blocked)", sec_examples)
    section("AGENTS.md", sec_agents)
    section("entry points, indexes, mirrors, profiles", sec_entry)
    section("operational templates", sec_templates)
    section("links and provenance", sec_links)
    section("notebook companions", sec_companions)
    section("frozen originals", sec_frozen)
    section("stand-up path (deterministic routing-table test)", sec_standup)
    section(f"Step 7 low-token simulation (budget {BUDGET})", sec_step7)
    after = tree_snapshot()
    diff = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    check("check run wrote nothing to the tree (idempotent)", not diff, ", ".join(diff[:8]) or f"{len(after)} files unchanged")
    if "--no-fixtures" not in sys.argv:
        section("validator fixtures (temp copies, no .git)", sec_fixtures)
    counts = {k: sum(r["status"] == k for r in results) for k in ("PASS", "FAIL", "BLOCKED")}
    print(f"\n{counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['BLOCKED']} BLOCKED")
    if "--report" in sys.argv:
        with open(sys.argv[sys.argv.index("--report") + 1], "w", encoding="utf-8") as f:
            json.dump({"counts": counts, "results": results}, f, indent=1)
    sys.exit(1 if counts["FAIL"] else 2 if counts["BLOCKED"] else 0)


if __name__ == "__main__":
    main()
