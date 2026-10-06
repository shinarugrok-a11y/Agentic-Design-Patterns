# Resource-Aware Optimization — patterns (Ch 16)

## Pattern
1. Classify query complexity cheaply.
2. Map class to model tier (fast/cheap vs. strong/expensive).
3. Run; optionally critique cheap answers.
4. Log cost and latency per tier.

## Prompt template
```
Classify the query as 'simple', 'reasoning', or 'internet_search'.
simple: direct factual or short answer. reasoning: multi-step logic or analysis.
internet_search: needs current information. Output only the label.
Query: {query}
```

## Key APIs
- ADK (book): Flash and Pro `Agent`s behind a `BaseAgent` router (word count < 20).
- OpenAI (book): gpt-4o classifier -> gpt-4o-mini / o4-mini / gpt-4o + web search.
- OpenRouter (book): `"model": "openrouter/auto"` or a `"models": [...]` fallback list.

## Pitfalls -> fixes
- Hard query labelled simple -> critic on cheap tier.
- Classifier too costly -> rules or tiny model.
- No metrics -> log per-tier cost/quality.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_16_*`.
