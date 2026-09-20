---
name: rag
description: Use when answers must ground in external documents or live sources. Do not use when model knowledge alone is sufficient and fresh.
role: [memory]
chapter: 14
token_cost_estimate: 191
chains_with: [tool-use, memory-management]
---

# Knowledge Retrieval (RAG)

## When to use
- Private docs or fresh facts needed
- Answers must cite sources
- Corpus is too large for context

## When NOT to use
- Stable public knowledge suffices
- No corpus or index exists
- Latency forbids retrieval

## Inputs
- Query plus corpus/index handle
- Top-K and distance threshold

## Outputs
- Ranked chunks with citations
- Answer grounded in chunks

## Failure modes
- Bad chunks — tune chunk size + top-K (start K=5)
- Stale index — version corpus, re-embed on change
- Citation drift — quote chunks, don't paraphrase blindly

## Minimal example
```python
chunks = retrieve(query, top_k=5)  # vector or search
answer = run(f"Answer {query} using only: {chunks}")
return with_citations(answer, chunks)
```

## Next skills
- If retrieval is one tool among many: load `tool-use`
- If persist what was learned: load `memory-management`
