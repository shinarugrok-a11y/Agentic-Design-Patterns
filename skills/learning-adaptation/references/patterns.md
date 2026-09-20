# Learning and Adaptation — patterns (Ch 9)

## Pattern
1. Define a measurable evaluator.
2. Generate candidates (prompt, code, policy) from the current best.
3. Score; keep only strict improvements.
4. Log history so regressions are visible.

## Prompt template
```
You improve a program for {metric}. Current best (score {score}):
{program}
Propose one focused change. Return only the full new program.
```

## Key APIs
- OpenEvolve: `OpenEvolve(program_path, evaluator_path, config)`; `run(iterations=)`.
- SICA: self-improving coding agent cycle (evaluate -> edit self -> re-evaluate).
- AlphaEvolve: LLM ensemble + evaluators as evolutionary search.

## Pitfalls -> fixes
- Reward hacking -> hold-out evaluation set.
- Broken tooling after self-edit -> sandbox + rollback.
- Forgetting -> keep an archive of past bests.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_09_*`.
