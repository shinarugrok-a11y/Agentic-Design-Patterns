# RAG patterns (Ch 14)

Three notebook variants: ADK Google Search agent, LangChain RAG pipeline, Vertex AI RAG memory.

Pattern A — ADK search agent: `Agent(name='research_assistant', model='gemini-2.0-flash-exp', instruction='…use Google Search…', tools=[Google Search])`.

Pattern B — LangChain pipeline: `TextLoader` -> `text_splitter` -> `OpenAIEmbeddings` -> `Weaviate` vectorstore -> retriever -> `ChatPromptTemplate | ChatOpenAI | StrOutputParser`. Full `typing` (`List, Dict, Any, TypedDict`) + `Document` handling.

Pattern C — Vertex AI: `VertexAiRagMemoryService` with `RAG_CORPUS_RESOURCE_NAME` + `SIMILARITY_TOP_K=5` (+ vector distance threshold).

Defaults: chunk ~500-1000 tokens, top-K 5, always return sources with the answer.

## Notebook extracts (on-demand detail)

### Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb

```python
search_agent = Agent(
instruction="You help users research topics. When asked, use the Google Search tool",
from google.adk.tools import Google Search
from google.adk.agents import Agent
```

### Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb

```python
class RAGGraphState(TypedDict):
def retrieve_documents_node(state: RAGGraphState) -> RAGGraphState:
def generate_response_node(state: RAGGraphState) -> RAGGraphState:
# Prompt template from the PDF
prompt = ChatPromptTemplate.from_template(template)
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OpenAIEmbeddings
```

### Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb

```python
RAG_CORPUS_RESOURCE_NAME = "projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id"
SIMILARITY_TOP_K = 5
rag_corpus=RAG_CORPUS_RESOURCE_NAME,
similarity_top_k=SIMILARITY_TOP_K,
# Import the necessary VertexAiRagMemoryService class from the google.adk.memory module.
from google.adk.memory import VertexAiRagMemoryService
# Define an optional parameter for the number of top similar results to retrieve.
# This controls how many relevant document chunks the RAG service will return.
```
