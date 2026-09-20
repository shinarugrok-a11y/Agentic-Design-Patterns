# Knowledge Retrieval (RAG) — Pattern reference

Load this file only when implementing `rag`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when answers need private, fresh, or specialized corpora beyond training data.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: RAG core concepts (chunking, embeddings, vector DB). Fig. 2: Agentic RAG. Fig. 3: Knowledge Retrieval pattern.

## Notebooks (extracted)

Knowledge Retrieval (RAG)

### Notebooks
- `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` ⚠️ thin
- `Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb`
- `Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb`

### Patterns
- **ADK Google Search:** minimal agent with search tool (search-augmented, not vector RAG)
- **LangChain + LangGraph:** load → chunk → embed (Weaviate) → retrieve node → generate node
- **Vertex AI RAG:** `VertexAiRagMemoryService` with corpus, `similarity_top_k`, `vector_distance_threshold`
- **Grounded generation:** "If you don't know the answer, just say that you don't know."

### Prompt templates
RAG QA template:
```
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:
```

### Minimal code
```python
# LangGraph RAG
workflow = StateGraph(RAGGraphState)
workflow.add_node("retrieve", retrieve_documents_node)
workflow.add_node("generate", generate_response_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
app = workflow.compile()
for s in app.stream({"question": "What did the president say about Justice Breyer"}):
    print(s)
```

```python
# ADK search agent (minimal)
search_agent = Agent(name="research_assistant", model="gemini-2.0-flash-exp",
                       instruction="Use the Google Search tool", tools=[Google Search])
```

### Caveats
- Google Search notebook is **very thin** (~284 chars) — 4 lines of code
- LangChain example downloads from GitHub URL (may get HTML not plain text)
- Weaviate embedded client + OpenAI embeddings required
- Vertex notebook is service setup only — no full agent loop
- Replace placeholder `RAG_CORPUS_RESOURCE_NAME`

---

## Failure modes (skill-level)
- Bad chunking → missed answers
- Generator ignores context or hallucinates
- HTML downloaded instead of source text

## Chains with
`memory-management`, `tool-use`
