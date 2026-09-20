# Memory patterns (Ch 8)

Five notebook variants: ADK session/memory services, LangChain history, LangGraph store.

ADK: `LlmAgent(output_key='last_greeting')` auto-writes state; tool-based writes via `ToolContext` (`log_user_login` updates `session.state`); `InMemorySessionService` (dev) vs `DatabaseSessionService('sqlite:///./my_agent_data.db')` vs `VertexAiSessionService` (prod); `InMemoryMemoryService` (ephemeral) vs `VertexAiRagMemoryService` (persistent searchable).

LangChain: `ChatMessageHistory` + `ConversationBufferMemory` + `LLMChain` with `{history}` slot; chat variant uses `MessagesPlaceholder`.

LangGraph: `InMemoryStore(index={'embed': embed})` with `(namespace, key)` search; `update_instructions` node rewrites stored instructions from conversation.

Rule: namespace every write `(app, user, session)`; prefer tool-mediated writes over freeform state edits.

## Notebook extracts (on-demand detail)

### Chapter_08_Memory_(ADK_Explicit_State_Update).ipynb

```python
def log_user_login(tool_context: ToolContext) -> dict:
from google.adk.tools.tool_context import ToolContext
from google.adk.sessions import InMemorySessionService
# --- Define the Recommended Tool-Based Approach ---
# Access the state directly through the provided context.
# Get current values or defaults, then update the state.
# This is much cleaner and co-locates the logic.
# In a real application, an LLM Agent would decide to call this tool.
# Here, we simulate a direct call for demonstration purposes.
import time
```

### Chapter_08_Memory_(ADK_LlmAgent_output_key).ipynb

```python
# Define an LlmAgent with an output_key.
greeting_agent = LlmAgent(
instruction="Generate a short, friendly greeting.",
output_key="last_greeting"
# Import necessary classes from the Google Agent Developer Kit (ADK)
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai.types import Content, Part
# Correctly check the state *after* the runner has finished processing all events.
```

### Chapter_08_Memory_(ADK_MemoryService_InMemory).ipynb

```python
RAG_CORPUS_RESOURCE_NAME = "projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id" # Replace with your Corpus resource name
SIMILARITY_TOP_K = 5 # Number of top results to retrieve
rag_corpus=RAG_CORPUS_RESOURCE_NAME,
similarity_top_k=SIMILARITY_TOP_K,
# This is suitable for local development and testing where data persistence
# across application restarts is not required. Memory content is lost when the app stops.
from google.adk.memory import InMemoryMemoryService
# Example: Using VertexAiRagMemoryService
```

### Chapter_08_Memory_(ADK_SessionService).ipynb

```python
# This is suitable for local development and testing where data persistence
# across application restarts is not required.
from google.adk.sessions import InMemorySessionService
# This is suitable for production or development requiring persistent storage.
# You need to configure a database URL (e.g., for SQLite, PostgreSQL, etc.).
from google.adk.sessions import DatabaseSessionService
# This is suitable for scalable production on Google Cloud Platform, leveraging
# Vertex AI infrastructure for session management.
```

### Chapter_08_Memory_(LangChain_LangGraph).ipynb

```python
# 1. Define LLM and Prompt
prompt = PromptTemplate.from_template(template)
ChatPromptTemplate,
SystemMessagePromptTemplate,
HumanMessagePromptTemplate,
# 1. Define Chat Model and Prompt
prompt = ChatPromptTemplate(
SystemMessagePromptTemplate.from_template("You are a friendly assistant."),
HumanMessagePromptTemplate.from_template("{question}")
def update_instructions(state: State, store: BaseStore):
```
