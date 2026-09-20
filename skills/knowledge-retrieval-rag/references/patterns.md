# Knowledge Retrieval (RAG) — Patterns

## Pattern variants
- **Standard RAG** — chunk, embed, vector-search top-k, append to prompt; the default when documents are independent.
- **Hybrid retrieval** — fuse BM25 keyword ranking with vector search; wins when queries carry exact identifiers that embeddings blur.
- **GraphRAG** — retrieve over a knowledge graph of entities and relations; wins on multi-hop questions needing facts stitched across documents, at higher maintenance cost.
- **Agentic RAG** — a reasoning layer validates sources, reconciles contradictions, decomposes into sub-queries, re-retrieves; wins when sources conflict or differ in vintage.
- **Search-tool grounding** — skip the index, give the agent a live search tool; open-web freshness, no corpus control.

## Prompt templates

```
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:
```

```
Sources with source name and date: {numbered_chunks}
Before answering, name any sources that contradict each other and say which you
trust and why (recency, authority, document type). Cite every claim as [n].
If the sources do not contain the answer, reply exactly: NOT IN CORPUS.
```

## Code patterns

LangChain + LangGraph (retrieve node, then generate node):
```python
chunks = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(documents)
vectorstore = Weaviate.from_documents(client=client, documents=chunks,
                                      embedding=OpenAIEmbeddings(), by_text=False)
retriever = vectorstore.as_retriever()

def retrieve_documents_node(state: RAGGraphState) -> RAGGraphState:
    return {"documents": retriever.invoke(state["question"]), **state}

def generate_response_node(state: RAGGraphState) -> RAGGraphState:
    context = "\n\n".join(d.page_content for d in state["documents"])
    rag_chain = ChatPromptTemplate.from_template(template) | llm | StrOutputParser()
    return {**state, "generation": rag_chain.invoke(
        {"context": context, "question": state["question"]})}

# StateGraph(RAGGraphState): entry "retrieve" -> "generate" -> END, then .compile()
```

Google ADK (live grounding; retrieval is just a tool):
```python
search_agent = Agent(name="research_assistant", model="gemini-2.0-flash-exp",
                     instruction="When asked, use the Google Search tool",
                     tools=[google_search])
```

Google ADK (managed corpus; the two knobs that govern recall vs. noise):
```python
memory_service = VertexAiRagMemoryService(
    rag_corpus=RAG_CORPUS_RESOURCE_NAME,
    similarity_top_k=5, vector_distance_threshold=0.7)
```

## Framework notes
- **LangChain / LangGraph** — `TextLoader` → `CharacterTextSplitter` → vector store → `as_retriever()`; making retrieve and generate `StateGraph` nodes is what enables re-retrieval loops.
- **Google ADK** — `google_search` for live grounding; `VertexAiRagMemoryService` for a managed corpus.

## Failure modes in depth
- **Retrieval misses, model guesses** — top-k too small or query phrased unlike the corpus; raise k behind a distance threshold, add BM25, and make "NOT IN CORPUS" an allowed answer.
- **Chunk size wrong** — small chunks lose the context that made them meaningful, large ones crowd the prompt with noise; chunk on structure (section, paragraph) with overlap, per the 500/50 default.
- **Stale index** — a pre-processed corpus drifts from evolving wikis; schedule reconciliation and carry a date in chunk metadata so the model prefers the current policy over a 2020 blog post.
- **Unattributable answers** — sources dropped between retrieval and generation; keep `doc.metadata["source"]` bound to each numbered chunk in the context string and require `[n]` citations.

## Source
Chapter 14 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb, Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb, Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb.
