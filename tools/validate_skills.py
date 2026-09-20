#!/usr/bin/env python3
"""Validate the skill library: manifest schema, token budgets, file layout.

Usage:
    python3 tools/validate_skills.py            # check only, non-zero exit on failure
    python3 tools/validate_skills.py --sync     # rewrite manifest token estimates
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "manifest.json"
ROLES = {"planner", "executor", "critic", "memory", "safety"}
SKILL_TOKEN_CAP = 400
REF_TOKEN_CAP = 1000
AGENTS_LINE_CAP = 60
LAZY_LOAD_BUDGET = 3000
REQUIRED_SECTIONS = [
    "## When to use",
    "## When NOT to use",
    "## Inputs",
    "## Outputs",
    "## Failure modes",
    "## Minimal example",
    "## Next skills",
]


def tokens(text):
    try:
        import tiktoken

        return len(tiktoken.get_encoding("cl100k_base").encode(text))
    except Exception:
        # Conservative fallback when tiktoken is unavailable.
        return max(len(text) // 4, int(len(text.split()) * 1.3))


def companion_name(rec):
    """Sibling card in chapter_notebooks/, one per chapter rather than per notebook."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", rec["name"]).strip("_")
    return f"Chapter_{rec['chapter']:02d}_{slug}.SKILL.md"


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).split("\n"):
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        fm[k.strip()] = v
    return fm, text[m.end():]


def main(sync=False):
    errors = []
    manifest = json.loads(MANIFEST.read_text())
    skills = manifest["skills"]
    ids = [s["id"] for s in skills]

    if len(set(ids)) != len(ids):
        errors.append("manifest: duplicate skill ids")
    if sorted(s["chapter"] for s in skills) != list(range(1, 22)):
        errors.append("manifest: chapters must cover 1-21 exactly once")

    measured = {}
    for rec in skills:
        sid = rec["id"]
        for key in ("name", "chapter", "role", "when_to_use", "when_not_to_use",
                    "inputs", "outputs", "failure_modes", "chains_with",
                    "token_cost_estimate"):
            if key not in rec:
                errors.append(f"{sid}: manifest missing '{key}'")
        if not set(rec.get("role", [])) <= ROLES:
            errors.append(f"{sid}: unknown role in {rec.get('role')}")
        if not 2 <= len(rec.get("failure_modes", [])) <= 4:
            errors.append(f"{sid}: failure_modes must hold 2-4 bullets")
        if not 2 <= len(rec.get("chains_with", [])) <= 3:
            errors.append(f"{sid}: chains_with must hold 2-3 ids")
        for dep in rec.get("chains_with", []):
            if dep not in ids:
                errors.append(f"{sid}: chains_with unknown id '{dep}'")

        skill_dir = ROOT / "skills" / sid
        skill_md = skill_dir / "SKILL.md"
        for rel in ("SKILL.md", "references/patterns.md", "examples/minimal.py"):
            if not (skill_dir / rel).is_file():
                errors.append(f"{sid}: missing {rel}")
        example = skill_dir / "examples" / "minimal.py"
        if example.is_file():
            try:
                proc = subprocess.run([sys.executable, "minimal.py"],
                                      cwd=example.parent, capture_output=True,
                                      text=True, timeout=30)
                if proc.returncode != 0:
                    errors.append(f"{sid}: examples/minimal.py exited "
                                  f"{proc.returncode}: "
                                  f"{proc.stderr.strip().splitlines()[-1:]}")
                elif not proc.stdout.strip():
                    errors.append(f"{sid}: examples/minimal.py printed nothing")
            except subprocess.TimeoutExpired:
                errors.append(f"{sid}: examples/minimal.py timed out")
        ref_md = skill_dir / "references" / "patterns.md"
        if ref_md.is_file():
            n_ref = tokens(ref_md.read_text())
            if n_ref > REF_TOKEN_CAP:
                errors.append(f"{sid}: references/patterns.md is {n_ref} tokens "
                              f"(cap {REF_TOKEN_CAP})")
        if not skill_md.is_file():
            continue

        text = skill_md.read_text()
        fm, body = frontmatter(text)
        if fm is None:
            errors.append(f"{sid}: SKILL.md has no YAML frontmatter")
            continue
        if fm.get("name") != sid:
            errors.append(f"{sid}: frontmatter name '{fm.get('name')}' != id")
        if fm.get("chapter") != str(rec["chapter"]):
            errors.append(f"{sid}: frontmatter chapter != manifest")
        if fm.get("role") != rec["role"]:
            errors.append(f"{sid}: frontmatter role != manifest")
        if fm.get("chains_with") != rec["chains_with"]:
            errors.append(f"{sid}: frontmatter chains_with != manifest")
        for section in REQUIRED_SECTIONS:
            if section not in body:
                errors.append(f"{sid}: SKILL.md missing '{section}'")

        n = tokens(text)
        measured[sid] = n
        if n > SKILL_TOKEN_CAP:
            errors.append(f"{sid}: SKILL.md is {n} tokens (cap {SKILL_TOKEN_CAP})")
        if not sync and abs(n - rec["token_cost_estimate"]) > 25:
            errors.append(
                f"{sid}: token_cost_estimate {rec['token_cost_estimate']} "
                f"drifted from measured {n}; rerun with --sync"
            )

        companion = ROOT / "chapter_notebooks" / companion_name(rec)
        if sync:
            companion.write_text(text)
        found = list((ROOT / "chapter_notebooks").glob(
            f"Chapter_{rec['chapter']:02d}_*.SKILL.md"))
        if not companion.is_file():
            errors.append(f"{sid}: missing companion {companion.name}")
        elif companion.read_text() != text:
            errors.append(f"{sid}: companion {companion.name} out of sync")
        if len(found) > 1:
            errors.append(f"{sid}: {len(found)} companions for chapter "
                          f"{rec['chapter']}, expected 1")

    agents = ROOT / "AGENTS.md"
    if not agents.is_file():
        errors.append("AGENTS.md missing")
    else:
        n_lines = len(agents.read_text().rstrip("\n").split("\n"))
        if n_lines > AGENTS_LINE_CAP:
            errors.append(f"AGENTS.md is {n_lines} lines (cap {AGENTS_LINE_CAP})")
    for profile in ("fable-5-1.md", "grok-4-6.md", "muse.md"):
        if not (ROOT / "models" / profile).is_file():
            errors.append(f"models/{profile} missing")

    if sync:
        for rec in skills:
            if rec["id"] in measured:
                rec["token_cost_estimate"] = measured[rec["id"]]
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
        print("synced token_cost_estimate for", len(measured), "skills")

    # Cold-start simulation, worst case per role:
    # AGENTS.md -> role-sliced index -> 2 SKILL.md -> 1 references/patterns.md.
    # Worst case picks the two largest cards and the largest references file in that role.
    route = tokens(agents.read_text()) if agents.is_file() else 0
    full_index = tokens(MANIFEST.read_text())
    # Same projection as the jq slice documented in AGENTS.md.
    slice_fields = ("id", "when_to_use")
    refs = {}
    for rec in skills:
        p = ROOT / "skills" / rec["id"] / "references" / "patterns.md"
        refs[rec["id"]] = tokens(p.read_text()) if p.is_file() else 0

    print(f"{'AGENTS.md':<26}{route:>6}")
    print(f"{'manifest.json (full)':<26}{full_index:>6}  tooling path, not cold start")
    if measured:
        print(f"{'all 21 SKILL.md':<26}{sum(measured.values()):>6}"
              f"  max {max(measured.values())}")
        print(f"{'all 21 patterns.md':<26}{sum(refs.values()):>6}"
              f"  max {max(refs.values())}")
    print(f"\n{'role':<10}{'slice':>7}{'2 cards':>9}{'1 ref':>7}{'total':>8}"
          f"  budget {LAZY_LOAD_BUDGET}")
    for role in sorted(ROLES):
        in_role = [s for s in skills if role in s.get("role", [])]
        if not in_role:
            continue
        slice_cost = tokens(json.dumps(
            [{k: s[k] for k in slice_fields if k in s} for s in in_role], indent=2))
        two_cards = sum(sorted(measured.get(s["id"], 0) for s in in_role)[-2:])
        worst_ref = max(refs.get(s["id"], 0) for s in in_role)
        total = route + slice_cost + two_cards + worst_ref
        print(f"{role:<10}{slice_cost:>7}{two_cards:>9}{worst_ref:>7}{total:>8}")
        if total > LAZY_LOAD_BUDGET:
            errors.append(f"worst-case {role} cold start is {total} tokens "
                          f"(budget {LAZY_LOAD_BUDGET})")

    if errors:
        print("\nFAIL")
        for e in errors:
            print("  -", e)
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sync="--sync" in sys.argv))
