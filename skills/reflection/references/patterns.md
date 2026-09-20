# Reflection — patterns (Ch 4)

## Pattern
1. Produce a draft.
2. Critique it against the task with an explicit stop token.
3. Refine using the critique; repeat up to N times.
4. Prefer a separate critic agent or model.

## Prompt template
```
Critic: You are a senior software engineer. Review the code against the task.
Task: {task}
Code: {code}
If flawless, respond ONLY with CODE_IS_PERFECT.
Otherwise list bugs, style issues, missing edge cases as bullets.
```

## Key APIs
- LangChain loop: `while i < max_iter: critique = llm(...); if 'CODE_IS_PERFECT' in critique: break`.
- ADK: `SequentialAgent([generator(output_key='draft'), reviewer(instruction='Review {draft}')])`.
- Single pass: `producer | critique_prompt | llm` for cheap one-shot review.

## Pitfalls -> fixes
- Endless loop -> stop token + max_iter.
- Vague critique -> demand numbered, actionable items.
- History overflow -> keep only latest draft + critique.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_04_*`.
