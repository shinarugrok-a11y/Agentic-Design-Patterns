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
- ADK: `LlmAgent(model='gemini-2.0-flash')` classifier, `gemini-2.5-pro` for reasoning, `google_search` tool for live data.
- Router: `{'simple': flash, 'reasoning': pro, 'internet_search': flash_search}[label]`.
- Cost: track tokens per tier; `usage_metadata` in responses.

## Pitfalls -> fixes
- Hard query labelled simple -> critic on cheap tier.
- Classifier too costly -> rules or tiny model.
- No metrics -> log per-tier cost/quality.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_16_*`.
