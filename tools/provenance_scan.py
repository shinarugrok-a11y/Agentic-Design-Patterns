#!/usr/bin/env python3
"""Line-level provenance scan of code blocks in skills/*/ markdown and examples.

For every fenced code block in skills/<id>/SKILL.md and references/*.md, each
code line with >= MIN_CHARS non-space characters is looked up (whitespace and
quote style normalised) in:
  GT-own   the book text slice for the skill's chapter
  NB-own   the code cells of that chapter's notebooks
  GT-other / NB-other  any other chapter or appendix
A line found nowhere is reported as "none" (our own code, or paraphrase).

This shows where code came from. It does not prove a block is verbatim: a
block can mix found and unfound lines. Read the flagged blocks by hand.

Usage: python3 tools/provenance_scan.py [--json out.json] [--skill id]
Stdlib only.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GT = os.path.join(ROOT, "ground-truth", "agentic_design_patterns.txt")
MIN_CHARS = 14
QUOTES = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u200b": ""})


def norm(s):
    return re.sub(r"\s+", "", s.translate(QUOTES))


def chapter_slices(lines):
    """Return {chapter_number or 'App': (start, end)} 0-based line ranges."""
    starts = []
    for i, l in enumerate(lines):
        m = re.match(r"^\f?Chapter (\d+): ", l)
        if m and not starts or (m and int(m.group(1)) == starts[-1][0] + 1):
            starts.append((int(m.group(1)), i))
    app = next(i for i, l in enumerate(lines) if l.lstrip("\f").startswith("Appendix A: "))
    out = {}
    for k, (ch, s) in enumerate(starts):
        e = starts[k + 1][1] if k + 1 < len(starts) else app
        out[ch] = (s, e)
    out["App"] = (app, len(lines))
    return out


def notebook_code(path):
    nb = json.load(open(path, encoding="utf-8"))
    return "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")


def load():
    lines = open(GT, encoding="utf-8").read().split("\n")
    sl = chapter_slices(lines)
    gt = {}
    for ch, (s, e) in sl.items():
        # keep a line-offset map so hits can be cited as GT line numbers
        txt, offs = "", []
        for i in range(s, e):
            n = norm(lines[i])
            offs.append((len(txt), i + 1))
            txt += n
        gt[ch] = (txt, offs)
    nbs = {}
    for p in glob.glob(os.path.join(ROOT, "chapter_notebooks", "*.ipynb")):
        b = os.path.basename(p)
        m = re.match(r"Chapter_(\d+)_", b)
        key = int(m.group(1)) if m else "App"
        nbs.setdefault(key, []).append((b, norm(notebook_code(p))))
    return sl, gt, nbs


def gt_line(gt_entry, idx):
    txt, offs = gt_entry
    line = offs[0][1]
    for o, ln in offs:
        if o > idx:
            break
        line = ln
    return line


def code_blocks(text):
    for m in re.finditer(r"^```[^\n]*\n(.*?)^```", text, re.S | re.M):
        start = text[: m.start()].count("\n") + 1
        yield start, m.group(1).splitlines()


def find(n, ch, gt, nbs):
    i = gt[ch][0].find(n) if ch in gt else -1
    if i >= 0:
        return "own", f"GT:L{gt_line(gt[ch], i)}"
    for b, code in nbs.get(ch, []):
        if n in code:
            return "own", b
    for k, entry in gt.items():
        if k != ch:
            j = entry[0].find(n)
            if j >= 0:
                return "other", f"Ch{k} GT:L{gt_line(entry, j)}"
    for k, lst in nbs.items():
        if k != ch:
            for b, code in lst:
                if n in code:
                    return "other", b
    return None, None


def classify(line, ch, gt, nbs):
    n = norm(line)
    if len(n) < MIN_CHARS:
        return None, None
    where, ref = find(n, ch, gt, nbs)
    if where:
        kind = "GT" if ref.startswith(("GT:", "Ch")) else "NB"
        return f"{kind}-{where}", ref
    # condensed lines: fall back to the longest literal / dotted identifier
    frags = sorted(re.findall(r"[\"']([^\"']{12,})[\"']|([A-Za-z_][\w.]{11,})", line),
                   key=lambda t: -len(t[0] or t[1]))
    for a, b in frags[:1]:
        where, ref = find(norm(a or b), ch, gt, nbs)
        if where:
            return f"frag-{where}", ref
    return "none", None


IDENT = re.compile(r"(?:from\s+([\w.]+)\s+import\s+([\w, ]+))|(?<![\w.])([A-Za-z_]\w*(?:\.\w+)*)\s*\(")
BUILTINS = set(dir(__builtins__)) | {"print", "len", "dict", "list", "set", "str", "int", "float", "range",
                                     "isinstance", "super", "sorted", "min", "max", "sum", "any", "all"}


def unknown_idents(blk, gt, nbs):
    """Called names / imports in a block that occur in no GT slice and no notebook."""
    corpus = [e[0] for e in gt.values()] + [c for lst in nbs.values() for _, c in lst]
    out = set()
    for ln in blk:
        if ln.lstrip().startswith("#"):
            continue
        for m in IDENT.finditer(ln):
            names = []
            if m.group(1):
                names = [m.group(1)] + [x.strip() for x in m.group(2).split(",") if x.strip()]
            elif m.group(3):
                names = [m.group(3).split(".")[-1]]
            for nm in names:
                if len(nm) < 4 or nm in BUILTINS:
                    continue
                if not any(nm in c for c in corpus):
                    out.add(nm)
    return sorted(out)


def scan(only=None):
    sl, gt, nbs = load()
    manifest = json.load(open(os.path.join(ROOT, "manifest.json"), encoding="utf-8"))
    report = []
    for s in manifest["skills"]:
        if only and s["id"] != only:
            continue
        ch = s["chapter"]
        files = [f"skills/{s['id']}/SKILL.md", f"skills/{s['id']}/references/patterns.md",
                 f"skills/{s['id']}/references/deep-dive.md"]
        for f in files:
            text = open(os.path.join(ROOT, f), encoding="utf-8").read()
            for start, blk in code_blocks(text):
                counts, where = {}, []
                for ln in blk:
                    c, w = classify(ln, ch, gt, nbs)
                    if c:
                        counts[c] = counts.get(c, 0) + 1
                        if w:
                            where.append(w)
                if counts:
                    report.append({"skill": s["id"], "chapter": ch, "file": f, "line": start,
                                   "counts": counts, "sources": sorted(set(where))[:6],
                                   "unknown_idents": unknown_idents(blk, gt, nbs)})
    return report


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--skill") + 1] if "--skill" in sys.argv else None
    rep = scan(only)
    if "--json" in sys.argv:
        json.dump(rep, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    for r in rep:
        c = r["counts"]
        tot = sum(c.values())
        flag = ""
        if any(k.endswith("-other") for k in c):
            flag += " OTHER-CHAPTER"
        if r["unknown_idents"]:
            flag += f" UNKNOWN-NAMES={r['unknown_idents']}"
        if c.get("none", 0) == tot:
            flag += " NO-SOURCE"
        elif c.get("none"):
            flag += " MIXED"
        print(f"{r['file']}:{r['line']}  {c}{flag}  {', '.join(r['sources'])}")
