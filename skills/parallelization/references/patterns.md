# Parallelization — patterns (Ch 3)

## Pattern
1. Identify branches that need only the shared input.
2. Run them concurrently; keep the original input alongside.
3. Synthesise with a prompt that only uses branch outputs.
4. Cap concurrency to respect rate limits.

## Prompt template
```
Based on the following information:
Summary: {summary}
Related Questions: {questions}
Key Terms: {key_terms}
Synthesize a comprehensive answer about {topic}. Use only the material above.
```

## Key APIs
- LangChain: `RunnableParallel(summary=c1, questions=c2, topic=RunnablePassthrough())` then `| synth | llm`.
- ADK: `SequentialAgent([ParallelAgent(sub_agents=[r1, r2, r3]), merger])`; each researcher sets `output_key`.
- Python: `asyncio.gather(*coros)`; in notebooks `nest_asyncio.apply()`.

## Pitfalls -> fixes
- Slow branch blocks join -> per-branch timeout and default value.
- Merge invents facts -> instruct 'use only the material above'.
- Shared mutable state -> pass results by return value/keys only.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_03_*`.
