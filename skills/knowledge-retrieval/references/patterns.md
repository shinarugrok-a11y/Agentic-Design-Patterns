# Knowledge Retrieval (RAG)

Ch 14.

## Frameworks
- LangChain (TextLoader, OpenAIEmbeddings, LangGraph RAG nodes); ADK (VertexAiRagMemoryService, google_search).

## Key APIs from the notebooks
- `LangChain: TextLoader -> OpenAIEmbeddings -> retriever; RAGGraphState with retrieve_documents_node + generate_response_node`
- `ADK: VertexAiRagMemoryService for managed retrieval`
- `ADK: google_search tool RAG variant for web-grounded answers`

## Code patterns
- Pattern: chunk + embed -> retrieve top-k -> generate with citations.
- LangGraph state: RAGGraphState carries docs between retrieve and generate nodes.
- Instruct 'use only the passages; cite sources' to curb hallucination.

## Prompt templates
- Grounded answer: `Answer using ONLY these passages. Cite [1][2]: {passages} \n Q: {query}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb`
- `chapter_notebooks/Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb`
- `chapter_notebooks/Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb`

