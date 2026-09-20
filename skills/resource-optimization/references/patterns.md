# Resource Optimization patterns (Ch 16)

Two notebooks: tier-selection snippets, OpenAI + Google Custom Search loop (`OI_Google_Search`).

Pattern A — Tier selection (conceptual): `Agent(name='GeminiProAgent', model='gemini-2.5-pro')` for hard queries vs cheap flash tier for triage; route by complexity signal. (`LiteLlm` wrapper for non-ADK models.)

Pattern B — Search-grounded cheap loop: `OpenAI` client + Google Custom Search (`GOOGLE_CUSTOM_SEARCH_API_KEY`, `GOOGLE_CSE_ID` via `.env` + `load_dotenv()`); small model + search beats big model alone on fresh facts.

Rules: define tier table first (model, cost, latency, quality bar); cache repeat queries; log spend per tier to prove savings.

## Notebook extracts (on-demand detail)

### Chapter_16_Resource_Optimization_(Code_Snippets).ipynb

```python
gemini_pro_agent = Agent(
instruction="You are an expert assistant for complex problem-solving."
gemini_flash_agent = Agent(
instruction="You are a quick assistant for straightforward questions."
class QueryRouterAgent(BaseAgent):
async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
# Conceptual Python-like structure, not runnable code
from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm # If using models not directly supported by ADK's default Agent
import asyncio
```

### Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb

```python
# --- Step 1: Classify the Prompt ---
def classify_prompt(prompt: str) -> dict:
def google_search(query: str, num_results=1) -> list:
def generate_response(prompt: str, classification: str, search_results=None) -> str:
def handle_prompt(prompt: str) -> dict:
from openai import OpenAI
"You are a classifier that analyzes user prompts and returns one of three categories ONLY:\n\n"
# Convert each search result dict to a readable string
# Remove or comment out the next line to avoid duplicate printing
# print("\n🔍 Search Results:", search_results)
```
