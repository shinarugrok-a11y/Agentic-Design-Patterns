---
name: rag
description: Retrieve then generate from a corpus. Use for private or fresh knowledge. Do NOT use when the question is closed-book trivia.
role: [memory]
chapter: 14
token_cost_estimate: 240
chains_with: [memory-management, tool-use]
---

# Knowledge Retrieval (RAG)

## When to use
- Answers need private, live, or specialist documents
- Standard pipeline: load → chunk → embed → retrieve → generate
- Must say "I don't know" when context is empty

## When NOT to use
- Closed-book generation is fine
- Need session prefs, not docs (load `memory-management`)
- Need web search as a tool, not a vector index (load `tool-use`)

## Inputs
- Corpus + embeddings/index
- Question
- `similarity_top_k` / distance threshold

## Outputs
- Retrieved passages
- Short grounded answer

## Failure modes
- Wrong chunk size / overlap
- Ungrounded generation
- Loader fetches HTML, not text

## Minimal example
```python
g = StateGraph(RAGState)
g.add_node("retrieve", retrieve_node)
g.add_node("generate", generate_node)
g.set_entry_point("retrieve")
g.add_edge("retrieve", "generate")
```

## Next skills
- If you need chat/session state: load `memory-management`
- If retrieval is a live search tool: load `tool-use`
