# Reflection patterns (Ch 4)

Three notebook variants: ADK `SequentialAgent` draft->critique, iterative loop with message history, LangChain generator-critic chains.

Pattern A — ADK `SequentialAgent([DraftWriter, FactChecker])`: generator `LlmAgent` writes with `output_key="draft_text"`; reviewer `LlmAgent` reads `state['draft_text']` and revises. Extend to 3 agents (draft -> critique -> revise).

Pattern B — Iterative loop: `SystemMessage` generator + `HumanMessage` critique in a `for` loop (max 3); stop on `clean` verdict. Keep full message history so the critic sees prior notes.

Pattern C — LangChain chains: generator chain (`ChatPromptTemplate | ChatOpenAI | StrOutputParser`) piped through a critic chain with `RunnablePassthrough`.

Prompt templates: critic prompt lists criteria (accuracy, clarity, completeness) and must output either PASS or numbered issues — never vague praise.

## Notebook extracts (on-demand detail)

### Chapter_04_Reflection_(ADK).ipynb

```python
generator = LlmAgent(
instruction="Write a short, informative paragraph about the user's subject.",
output_key="draft_text" # The output is saved to this state key.
reviewer = LlmAgent(
instruction="""
output_key="review_output" # The structured dictionary is saved here.
# The SequentialAgent ensures the generator runs before the reviewer.
review_pipeline = SequentialAgent(
from google.adk.agents import SequentialAgent, LlmAgent
# The first agent generates the initial draft.
```

### Chapter_04_Reflection_(Iterative_Loop).ipynb

```python
def run_reflection_loop():
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
# Load environment variables from .env file (for OPENAI_API_KEY)
# Initialize the Chat LLM. We use a powerful model like gpt-4o for better reasoning.
# A lower temperature is used for more deterministic and focused outputs.
# We will build a conversation history to provide context in each step.
# The first message is just the task prompt.
import os
```

### Chapter_04_Reflection_(LangChain).ipynb

```python
ChatPromptTemplate.from_messages([
ChatPromptTemplate.from_messages([
ChatPromptTemplate.from_messages([
RunnablePassthrough.assign(
| RunnablePassthrough.assign(
async def run_reflection_example(product_details: str):
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
```
