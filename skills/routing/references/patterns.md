# Routing — patterns (Ch 2)

## Pattern
1. Describe each handler in one line (what it does, when to pick it).
2. Classify the request into exactly one label with an `unclear` fallback.
3. Dispatch to the handler; normalise the label first.
4. Handlers may themselves be chains or agents.

## Prompt template
```
Analyze the request and pick the handler.
- Booking flights or hotels: 'booker'. - General questions: 'info'.
- Unclear or neither: 'unclear'.
ONLY output one word.
```

## Key APIs
- LangChain: `RunnableBranch((lambda x: x['decision'] == 'booker', booker_chain), ..., default)`.
- ADK: `Agent(name="Coordinator", sub_agents=[booker, info])` auto-delegates on sub-agent `description`.
- OpenRouter: one endpoint, `model=` selects provider; route by cost/quality tier.

## Pitfalls -> fixes
- Overlapping handler descriptions -> make them mutually exclusive.
- Label drift (`' Booker\n'`) -> `.strip().lower()`.
- No fallback -> always define an `unclear` handler.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_02_*`.
