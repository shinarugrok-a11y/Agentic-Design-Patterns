# Repository evidence audit (2026-09-23)

Independent evidence track for this repository. Claude/Anthropic extraction outputs were not used as authority.

Another agent should be able to answer: what does this repository implement, where is the evidence, what is verified, what remains uncertain, and what should not be trusted?

| Deliverable | File |
| --- | --- |
| 1. Structural map | [01-structural-map.md](01-structural-map.md) |
| 2. Evidence map | [02-evidence-map.md](02-evidence-map.md), [evidence-claims.json](evidence-claims.json), [notebook-inventory.json](notebook-inventory.json) |
| 3. Documentation accuracy | [03-documentation-accuracy.md](03-documentation-accuracy.md) |
| 4. Correction log | [04-correction-log.md](04-correction-log.md) |
| 5. Dependency and dead-material report | [05-dependency-dead-material.md](05-dependency-dead-material.md) |
| 6. Candidate pattern mappings | [06-candidate-pattern-mappings.md](06-candidate-pattern-mappings.md) |
| 7. Security findings | [07-security-findings.md](07-security-findings.md) |
| 8. Folder-tree architecture | [08-folder-tree-architecture.md](08-folder-tree-architecture.md) |
| 9. Consistency report | [09-consistency-report.md](09-consistency-report.md) |
| 10. Unresolved items | [10-unresolved.md](10-unresolved.md) |
| 11. README | [`README.md`](../../README.md) at the repository root |

## Method

Inspection of the tree at the start of this audit (`main` = `ed9027e`), then:

- `pdfinfo` (Poppler 24.02.0) on `Agentic_Design_Patterns_Complete.pdf`
- `pdftotext -layout` compared with `ground-truth/agentic_design_patterns.txt`
- `python3 tools/validate.py` (after `tiktoken` 0.14.0 was installed in the audit environment; it is not a repo lockfile)
- `ast.parse` of each notebook code cell
- Offline execution of notebook cells whose imports are standard-library only and that do not reference the network
- Git history (`git log`, `git shortlog`) and GitHub API reads for this repository and `evoiz/Agentic-Design-Patterns`
- Pattern scan of the working tree for common secret shapes (`sk-…`, `AIza…`, `AKIA…`, private-key blocks): no matches

No live model API was called. No Google Drive login was performed.
