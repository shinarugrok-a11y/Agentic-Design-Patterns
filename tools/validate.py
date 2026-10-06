#!/usr/bin/env python3
"""Validate the skill library and run the low-token agent simulation.

Usage: python3 tools/validate.py            check only, non-zero exit on failure
       python3 tools/validate.py --sync     first refresh token_cost_estimate in
                                            SKILL.md + manifest.json, rewrite the
                                            notebook companions, both INDEX.md
                                            files and .agents/skills, then check
Requires: pip install tiktoken

Checks structure, manifest <-> SKILL.md consistency, token caps, notebook
companions, that examples run offline, and that AGENTS.md + skills/INDEX.md +
the boot templates + any two same-role SKILL.md files + one references/patterns.md stays < 3000
tokens for every role pair (the Step 7 gate). The base is what bots read at boot:
AGENTS.md + skills/INDEX.md + every templates/*.md linked from AGENTS.md (the
gates); it was AGENTS.md + manifest.json before the slim index existed.

Boot path: AGENTS.md is the single entry point with ordered boot steps, each
with a Done: check; its profile table has a fallback and every profile exists;
skills/INDEX.md and ground-truth/INDEX.md equal their generated renders; the
index lists each manifest id once with the manifest roles; GEMINI.md points at
AGENTS.md; there is no CLAUDE.md; .agents/skills/<id> symlinks resolve; links
and repo paths in the boot docs and models/ resolve; every deep-dive code block
carries a Provenance line; the worst-case stand-up load fits the AGENTS.md
budget; and the fixtures in tests/fixtures/standup_tasks.json pass
(tools/standup_sim.py, a deterministic routing-table test).

The Step 7 gate is an invariant, not a description of the current result.
Do not raise BUDGET to make a failure pass; trim AGENTS.md, the index signals or
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


# --- manifest -------------------------------------------------------------
manifest = json.loads(read("manifest.json"))
if "--sync" in sys.argv:
    sync(manifest)
    manifest = json.loads(read("manifest.json"))
skills = manifest["skills"]
ids = [s["id"] for s in skills]
patterns = [s for s in skills if s.get("kind") == "pattern"]
operational = [s for s in skills if s.get("kind") == "operational"]
check("manifest kinds are pattern or operational", len(patterns) + len(operational) == len(skills))
check("manifest has 21 pattern skills (one per chapter)", len(patterns) == 21, str(len(patterns)))
check("operational skills have chapter null", all(s["chapter"] is None for s in operational),
      ", ".join(s["id"] for s in operational))
check("manifest ids unique + kebab-case",
      len(set(ids)) == len(ids) and all(isinstance(i, str) and ID_RE.fullmatch(i) for i in ids))
check("pattern skill chapters are exactly 1..21",
      sorted(s["chapter"] for s in patterns if type(s["chapter"]) is int) == list(range(1, 22)))
required = {"id", "name", "chapter", "role", "when_to_use", "when_not_to_use", "inputs", "outputs",
            "failure_modes", "chains_with", "token_cost_estimate", "kind", "signals"}
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
                          and fm.get("kind", "pattern") == s["kind"]
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
skill_dirs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "skills", "*")) if os.path.isdir(p))
check("skill directories are exactly the manifest ids", skill_dirs == sorted(ids),
      f"extra={sorted(set(skill_dirs) - set(ids))} missing={sorted(set(ids) - set(skill_dirs))}")

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
for kw in ("skills/INDEX.md", "Do not load the entire PDF", "Do not load all skills", "models/", "GEMINI.md"):
    check(f"AGENTS.md contains '{kw}'", kw in agents)
steps = re.split(r"^(?=\d+\. \*\*)", agents.split("## Boot", 1)[-1].split("\n## ", 1)[0], flags=re.M)[1:]
check("AGENTS.md has >= 5 ordered boot steps, each with a Done: check",
      len(steps) >= 5 and all("Done:" in st for st in steps)
      and [int(st.split(".", 1)[0]) for st in steps] == list(range(1, len(steps) + 1)), f"{len(steps)} steps")

# --- entry points, generated indexes, mirrors ------------------------------
sys.path.insert(0, os.path.join(ROOT, "tools"))
import standup_sim  # noqa: E402

std = standup_sim.parse_standup()
std_profiles = sorted({p for _, p in std["profiles"]})
check("AGENTS.md profile table has a fallback (*) row", any("*" in sig for sig, _ in std["profiles"]))
check(f"{INDEX_PATH} matches render from manifest.json (run --sync)",
      os.path.exists(os.path.join(ROOT, INDEX_PATH)) and read(INDEX_PATH) == render_index(manifest))
check(f"{GT_INDEX_PATH} matches render from the ground-truth text (run --sync)",
      os.path.exists(os.path.join(ROOT, GT_INDEX_PATH)) and read(GT_INDEX_PATH) == render_gt_index())
gemini = read("GEMINI.md") if os.path.exists(os.path.join(ROOT, "GEMINI.md")) else ""
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

# --- models ---------------------------------------------------------------
for p in sorted(set(std_profiles) | {f"models/{m}.md" for m in ("fable-5-1", "grok-4-6", "muse")}):
    n = read(p).count("\n") if os.path.exists(os.path.join(ROOT, p)) else 0
    check(f"{p} exists, 30-50 lines" + (" (named in AGENTS.md)" if p in std_profiles else ""),
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
tmpl_missing = [t for t in TEMPLATES if not os.path.exists(os.path.join(ROOT, t))]
check("operational templates exist and are labelled DERIVED/operational",
      not tmpl_missing and all("DERIVED/operational" in read(t) for t in TEMPLATES), ", ".join(tmpl_missing))
check("AGENTS.md boot path links templates/gates.md", "templates/gates.md" in std["always"])
gates_text = read("templates/gates.md") if "templates/gates.md" not in tmpl_missing else ""
check("gates template has G1-G7 and ship = NO default",
      all(f"| G{k} |" in gates_text for k in range(1, 8)) and "`ship = NO`" in gates_text)
env_lines = [l for l in read(".env.example").splitlines() if l.strip() and not l.startswith("#")] \
    if os.path.exists(os.path.join(ROOT, ".env.example")) else None
check(".env.example exists with empty placeholders only",
      env_lines is not None and all(re.fullmatch(r"[A-Z][A-Z0-9_]*=", l) for l in env_lines),
      "missing" if env_lines is None else ", ".join(l for l in env_lines if not re.fullmatch(r"[A-Z][A-Z0-9_]*=", l)))
model_files = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "models", "*.md")))
no_gate_ptr = [m for m in model_files if "templates/gates.md" not in read(m)]
check("every models/*.md points its gate rules at templates/gates.md", not no_gate_ptr, ", ".join(no_gate_ptr))

MUST_NOT_EXIST = {"CLAUDE.md"}
link_bad = []
docs = ["AGENTS.md", "GEMINI.md", INDEX_PATH] + sorted(set(std["always"]) | set(TEMPLATES)) + sorted(
    os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "models", "*.md")))
for doc in docs:
    if not os.path.exists(os.path.join(ROOT, doc)):
        link_bad.append(f"{doc} (missing)")
        continue
    text = read(doc)
    targets = re.findall(r"\]\(([^)\s#]+)", text)
    targets += [t for t in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|json|py))`", text) if "/" in t or t[0].isupper()]
    for t in targets:
        if t.startswith(("http://", "https://", "mailto:")) or "<" in t or "*" in t or t in MUST_NOT_EXIST:
            continue
        if t.startswith(("references/", "examples/")):
            if not all(os.path.exists(os.path.join(ROOT, "skills", i, t)) for i in ids):
                link_bad.append(f"{doc}: {t} (missing in some skills/<id>/)")
            continue
        if not os.path.exists(os.path.normpath(os.path.join(ROOT, os.path.dirname(doc), t))) \
                and not os.path.exists(os.path.join(ROOT, t)):
            link_bad.append(f"{doc}: {t}")
check("links and repo paths in AGENTS.md, GEMINI.md, the index, templates and models/ resolve",
      not link_bad, "; ".join(link_bad))

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
by_chapter = {s["chapter"]: s["id"] for s in patterns}
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
print(f"\n=== Stand-up simulation (cl100k_base tokens, AGENTS.md budget {std['budget']}) ===")
su_files = standup_sim.BOOT_FILES + std["always"]
su_base = sum(standup_sim.tokens(f) for f in su_files)
su_prof = max((standup_sim.tokens(p), p) for p in std_profiles)
su_top = sorted(full_tok.values(), reverse=True)[:standup_sim.MAX_SKILLS]
su_worst = su_base + su_prof[0] + sum(su_top)
print("boot files: " + ", ".join(f"{f} {standup_sim.tokens(f)}" for f in su_files))
print(f"worst case: base {su_base} + {su_prof[1]} {su_prof[0]} + {standup_sim.MAX_SKILLS} heaviest SKILL.md "
      f"{sum(su_top)} = {su_worst} (headroom {std['budget'] - su_worst})")
check(f"stand-up worst case <= budget {std['budget']}", su_worst <= std["budget"], f"{su_worst} tokens")
for r in standup_sim.simulate():
    print(f"  {r['id']:20} profile={os.path.basename(r['profile'])} skills={r['skills']} tokens={r['tokens']}"
          + (f" hitl={r['hitl']['statuses']}" if r["hitl"] else ""))
    check(f"fixture {r['id']}", r["pass"], "; ".join(r["fails"]))

# --- Step 7: low-token agent simulation -----------------------------------
print(f"\n=== Low-token agent simulation (cl100k_base tokens, budget {BUDGET}) ===")
index_tok = tok(read(INDEX_PATH))
gates_tok = sum(tok(read(f)) for f in std["always"])
base = tok(agents) + index_tok + gates_tok
print(f"AGENTS.md        {tok(agents):>5}\nskills/INDEX.md  {index_tok:>5}\n"
      f"{' + '.join(std['always']) or 'boot templates':16} {gates_tok:>5}\nbase             {base:>5}"
      f"\n(manifest.json {tok(read('manifest.json'))} is for tools and not on the boot path)")
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
print(f"executor walk-through: {tok(agents)} + {index_tok} + {gates_tok} + {full_tok['prompt-chaining']} "
      f"+ {full_tok['tool-use']} + {pat_tok['tool-use']} = {ex}")
check(f"simulation: executor walk-through < {BUDGET}", ex < BUDGET, f"{ex} tokens")
check(f"simulation: every role pair + one patterns.md < {BUDGET}", worst[0] < BUDGET, f"worst {worst[0]} tokens")

print(f"\n{'id':30}{'body':>6}{'SKILL.md':>10}{'patterns':>10}")
for s in skills:
    print(f"{s['id']:30}{body_tok[s['id']]:>6}{full_tok[s['id']]:>10}{pat_tok[s['id']]:>10}")
fails = sum(1 for _, ok in results if not ok)
print(f"\n{len(results) - fails} passed, {fails} failed")
sys.exit(1 if fails else 0)
