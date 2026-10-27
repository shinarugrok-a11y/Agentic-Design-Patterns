# 8. Folder-tree architecture

## What was kept

The tree already separated source, derived skills, notebooks, and tooling. Mass moves would rewrite history for no gain in evidence. These paths stay where they are:

| Concern | Path | Why it stays |
| --- | --- | --- |
| Authoritative book bytes | `Agentic_Design_Patterns_Complete.pdf` | One blob since `7ddebbc`. Moving it would break `ground-truth/README.md` and the validator's PDF guard. |
| Authoritative text | `ground-truth/` | Named for audits. Already not mixed into `skills/`. |
| Derived pattern cards | `skills/<id>/` | One directory per chapter. `AGENTS.md` and `manifest.json` depend on this layout. |
| Agent entry | `AGENTS.md`, `manifest.json`, `models/` | Small root files an agent can load without walking notebooks. |
| Book code mirror | `chapter_notebooks/` | Historical filenames are the citation keys. |
| Checks | `tools/validate.py` | Single executable check. |
| Evidence | `validation/audit/` | Added here so audit notes are not mixed into `skills/` or the PDF extract. |

## What was not created

A `source/`, `patterns/`, `implementations/`, `code/`, `appendices/`, `historical/`, or `tests/` split was considered and not applied.

- The PDF is the source. A `source/` directory would be a move.
- `skills/` is already the pattern layer.
- `chapter_notebooks/` is the implementation mirror, with the caveat that much of it does not run.
- There is no separate `code/` package.
- Appendix prose is inside the PDF. The appendix ipynb files are mostly placeholders; moving them to `historical/` would touch frozen notebooks.
- `tools/validate.py` is the test. A new `tests/` wrapper would duplicate it.

## How to navigate

```
repository/
├── README.md                 public contract (status, provenance, limits)
├── Agentic_Design_Patterns_Complete.pdf
├── ground-truth/             text extract of that PDF
├── skills/                   derived cards + offline examples
├── models/                   unverified loading notes
├── chapter_notebooks/        snippets, fragments, 7 historical placeholders
├── tools/validate.py
└── validation/
    └── audit/                this evidence pass
```

## Boundaries an agent should respect

- Book claims: prefer `ground-truth/agentic_design_patterns.txt`, and remember 17 lines differ from Poppler 24.02.0.
- Pattern behavior that has been executed: `skills/<id>/examples/minimal.py`.
- Pattern behavior that is only described: `skills/<id>/SKILL.md` and `references/`.
- Notebook cells: examples and fragments, including known syntax errors. Not the verification suite.
- `chapter_notebooks/*.SKILL.md`: generated copies. Edit `skills/` and re-run `python3 tools/validate.py --sync` if a copy must change.
- `validation/audit/`: classifications and measurements. Not a second source of the book.
