---
name: rag
description: Retrieve top-k chunks and ground the answer. Use for large or changing corpora. Not when the corpus fits in context.
role: [memory]
chapter: 14
token_cost_estimate: 194
chains_with: [memory-management, reflection]
---

# Knowledge Retrieval

## When to use
- Corpus is large or changes often.
- Answers must cite sources.
- Private or recent facts the model lacks.

## When NOT to use
- Corpus fits in the prompt.
- Question is general knowledge.

## Inputs
- Query
- Indexed chunks (vector store)

## Outputs
- Grounded answer
- Cited chunks

## Failure modes
- Bad chunking splits facts.
- Irrelevant top-k, answer hallucinates.
- Stale index.

## Minimal example
```python
docs = retriever.invoke(query)                       # top-k chunks
ctx = "\n".join(d.page_content for d in docs)
answer = llm(f"Answer only from context; say 'unknown' otherwise.\n{ctx}\nQ: {query}")
```

## Next skills
- If retrieved facts must persist: load `memory-management`
- If answer needs verification: load `reflection`
