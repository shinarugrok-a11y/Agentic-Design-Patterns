# Goal Setting and Monitoring — patterns (Ch 11)

## Pattern
1. Write goals as checkable statements.
2. Generate; critique against goals; judge boolean.
3. Stop on all-met or max iterations.
4. Report status per goal.

## Prompt template
```
Goals: {goals}
Judge: Does the code satisfy ALL goals? Reply exactly 'True' or 'False'.
Critic: For each goal, state met/unmet and why in one line.
```

## Key APIs
- Loop: `generate -> critique -> judge` with `max_iterations`.
- Judge prompt returns a strict boolean token; parse with `.strip() == 'True'`.
- Store per-goal status as JSON for monitoring.

## Pitfalls -> fixes
- Judge waffles -> force True/False only.
- Conflicting goals -> rank or drop.
- No cap -> `max_iterations`.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_11_*`.
