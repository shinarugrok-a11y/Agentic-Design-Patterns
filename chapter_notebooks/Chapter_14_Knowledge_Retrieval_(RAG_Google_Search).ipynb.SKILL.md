---
name: knowledge-retrieval
description: Retrieve relevant documents then generate grounded answers.
role: [memory]
chapter: 14
token_cost_estimate: 223
chains_with: [memory-management, tool-use]
---

# Knowledge Retrieval (RAG)

## When to use
- Answers need private, recent, or cited knowledge.
- Corpus can be chunked, embedded, and searched.
- Every claim should trace to retrieved passages.

## When NOT to use
- Answer is stable public knowledge the model knows.
- Corpus is tiny; stuff it in context instead.

## Inputs
- Query + corpus
- Top-k + citation requirement

## Outputs
- Grounded answer with source citations

## Failure modes
- Retriever returns irrelevant chunks; answer hallucinates anyway.
- Stale index serves outdated facts.
- Over-retrieval drowns the prompt in noise.

## Minimal example
```python
docs = retrieve(query, top_k=5)  # TextLoader+embeddings / VertexAiRag
answer = llm(f"Answer {query} using only: {docs}\nCite sources.")
```

## Next skills
- If retrieved facts must persist across turns: load `memory-management`
- If retrieval is one tool among many: load `tool-use`
