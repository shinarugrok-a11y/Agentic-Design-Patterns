# Knowledge Retrieval — patterns (Ch 14)

## Pattern
1. Chunk documents; embed; index.
2. Retrieve top-k for the query.
3. Answer strictly from retrieved context; cite.
4. Refresh the index when sources change.

## Prompt template
```
You are a helpful assistant. Answer ONLY from the context below.
If the answer is not in the context, say you do not know.
Context:
{context}
Question: {question}
```

## Key APIs
- LangChain: `RecursiveCharacterTextSplitter`, `WeaviateVectorStore`, `retriever.invoke(q)`.
- LangGraph: `retrieve -> generate` graph with `StateGraph`.
- ADK: `VertexAiRagMemoryService`, `VSearchAgent` for managed retrieval.

## Pitfalls -> fixes
- Facts split across chunks -> overlap + larger chunks.
- Irrelevant top-k -> rerank or hybrid search.
- Stale index -> scheduled re-index.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_14_*`.
