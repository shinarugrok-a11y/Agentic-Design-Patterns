# Knowledge Retrieval (RAG) — reference patterns

Source: Chapter 14 + `Chapter_14_Knowledge_Retrieval_(RAG_LangChain)`,
`(RAG_Google_Search)`, `(RAG_VertexAI)`.

## Pipeline (book)
1. **Chunk** documents (size/overlap tuned to the content).
2. **Embed** chunks; store in a vector DB (semantic search by meaning).
3. **Retrieve** top-k chunks for the query (plus optional hybrid keyword search).
4. **Augment** the prompt with the retrieved context.
5. **Generate** a grounded answer, citing sources.

Variants: **GraphRAG** (knowledge graph for multi-hop relationships),
**Agentic RAG** (an agent validates, reconciles conflicting sources, runs
multi-step queries and calls tools to fill gaps).
Benefits: fresh/private knowledge, fewer hallucinations, attributable
answers. Costs: chunking quality, retrieval relevance, added latency.

## Notebook pattern: LangChain + Weaviate + LangGraph
```python
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import OpenAIEmbeddings
from langgraph.graph import StateGraph, END

loader = TextLoader("./state_of_the_union.txt")
documents = loader.load()
chunks = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(documents)

client = weaviate.Client(embedded_options=EmbeddedOptions())
vectorstore = Weaviate.from_documents(client=client, documents=chunks,
                                      embedding=OpenAIEmbeddings(), by_text=False)
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

class RAGGraphState(TypedDict):
    question: str
    documents: List[Document]
    generation: str

def retrieve_documents_node(state):
    documents = retriever.invoke(state["question"])
    return {"documents": documents, "question": state["question"], "generation": ""}

def generate_response_node(state):
    template = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:
"""
    context = "\n\n".join(doc.page_content for doc in state["documents"])
    rag_chain = ChatPromptTemplate.from_template(template) | llm | StrOutputParser()
    generation = rag_chain.invoke({"context": context, "question": state["question"]})
    return {**state, "generation": generation}

workflow = StateGraph(RAGGraphState)
workflow.add_node("retrieve", retrieve_documents_node)
workflow.add_node("generate", generate_response_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
app = workflow.compile()
for s in app.stream({"question": "What did the president say about Justice Breyer"}): print(s)
```
The graph makes it easy to insert nodes later: query rewriting, relevance
grading, web fallback (Agentic RAG).

## ADK options
```python
# Web grounding via search tool
search_agent = Agent(name="research_assistant", model="gemini-2.0-flash-exp",
    instruction="You help users research topics. When asked, use the Google Search tool",
    tools=[google_search])

# Managed RAG corpus as memory
from google.adk.memory import VertexAiRagMemoryService
memory_service = VertexAiRagMemoryService(
    rag_corpus="projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id",
    similarity_top_k=5,               # how many chunks to return
    vector_distance_threshold=0.7)    # filter weak matches

# Enterprise datastore agent (see tool-use): agents.VSearchAgent(datastore_id=...)
```

## Grounded-answer prompt template
```
Answer ONLY from the context. If the context is insufficient, say "I don't know".
Cite the chunk ids you used in [brackets].
Question: {question}
Context:
[1] {chunk_1}
[2] {chunk_2}
```

## Tuning knobs
| Knob | Effect |
|---|---|
| chunk_size / overlap | too small loses context; too large dilutes relevance |
| top_k | recall vs. prompt size |
| distance threshold | precision; empty result must be handled |
| hybrid search | keyword + vector for exact identifiers |
| re-ranker | improves ordering of top-k |
| query rewrite | handles vague or multi-part questions |

## Failure diagnostics
- Wrong answer but right chunk present -> prompt problem.
- Right chunk absent -> chunking/embedding/top_k problem.
- Confident answer with no chunks -> missing "I don't know" instruction.
- Stale answers -> index not refreshed after document updates.
