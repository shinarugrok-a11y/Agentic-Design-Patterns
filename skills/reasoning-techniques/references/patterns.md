# Reasoning Techniques — patterns (Ch 17)

## Pattern
1. Pick a technique: CoT (linear), ToT (search), ReAct (act+observe), self-correction.
2. Give a step budget.
3. Separate reasoning trace from final answer.
4. Verify the answer with a second pass.

## Prompt template
```
Think step by step. Show your reasoning, then write 'Answer:' followed by the final answer only.
ReAct: Thought: ... Action: <tool>[args] Observation: ... repeat, then Final Answer: ...
```

## Key APIs
- CoT/ToT: prompt-only; ToT branches evaluated by a scoring prompt.
- ReAct: LangChain `create_react_agent`; ADK `LlmAgent` with tools and iterative events.
- Related: Chain of Debates, PAL (program-aided), scaling inference compute.

## Pitfalls -> fixes
- Confident wrong chain -> self-correction pass.
- ToT explosion -> beam width + depth caps.
- Trace in output -> parse after 'Answer:'.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_17_*`.
