---
name: knowledge-retrieval-rag
description: Ground answers in retrieved external text. Retrieve relevant external snippets and append them to the prompt so answers are grounded and citable. Skip it when the answer needs no external facts or the corpus is small enough to pass inline.
role: [memory]
chapter: 14
token_cost_estimate: 370
chains_with: [memory-management, reflection, tool-use]
---

# Knowledge Retrieval (RAG)

## When to use
- Answers need current or proprietary facts
- Claims must be attributable to sources
- The corpus is too large to pass inline

## When NOT to use
- Facts are already in context or in-model
- Freshness and citation do not matter
- The index cannot be kept up to date

## Inputs
- user query
- indexed corpus or search tool
- top-k and chunking configuration

## Outputs
- retrieved chunks with sources
- grounded answer
- citations

## Failure modes
- Retrieval misses the answer, so the model fills the gap by guessing
- Chunks too small to carry context or too large to fit
- Stale index served as current fact
- Answer not attributable because sources are dropped

## Minimal example
```python
docs = retriever.invoke(query)                  # top-k, chunked with overlap
context = "\n\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs))
answer = llm.invoke(RAG_PROMPT.format(context=context, question=query))
cite(answer, [d.metadata["source"] for d in docs])  # no sources, no answer
```

## Next skills
- If recall must persist per user: load `memory-management`
- If groundedness needs checking: load `reflection`
- If retrieval is a live API: load `tool-use`
