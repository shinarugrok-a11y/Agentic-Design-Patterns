---
name: rag
description: Retrieve relevant chunks, augment the prompt, generate grounded answers. Answer from external or proprietary documents by retrieving top-k chunks and grounding the prompt in them. Do not use when the model's training knowledge suffices or when the corpus is tiny enough to fit in context.
role: [memory]
chapter: 14
token_cost_estimate: 340
chains_with: [memory-management, tool-use, reasoning-techniques]
---

# Knowledge Retrieval (RAG)

## When to use
- Facts are private, recent or domain-specific.
- Answers must cite sources.
- Corpus is too big for the context window.
- Hallucination rate must drop.

## When NOT to use
- General knowledge questions.
- Corpus < a few pages: paste it in.
- Need is conversational history, not documents: use `memory-management`.

## Inputs
- Document corpus
- Chunking params (size, overlap)
- Embedding model + vector store
- Query

## Outputs
- Retrieved documents
- Grounded answer
- Citations/grounding metadata

## Failure modes
- Bad chunking splits the fact across chunks.
- Retriever returns irrelevant top-k; model answers anyway.
- Prompt lacks 'say I don't know'; hallucination persists.
- Embedding model changed; index stale.

## Minimal example
```python
chunks = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
retriever = VectorStore.from_documents(chunks, embedding).as_retriever()
prompt = "Use only this context. If unknown say so. Q: {question}\nContext: {context}"
graph: retrieve(question)->documents ; generate(documents)->answer
# ADK: VSearchAgent(datastore_id=...); VertexAiRagMemoryService(rag_corpus=...)
```

## Next skills
- If retrieved facts should persist as memory: load `memory-management`
- If retrieval is a search tool call: load `tool-use`
- If agent should validate/reconcile retrieved evidence: load `reasoning-techniques`
