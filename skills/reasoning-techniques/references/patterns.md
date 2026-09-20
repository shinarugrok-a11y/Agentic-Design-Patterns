# Reasoning patterns (Ch 17)

Four notebook variants: CoT retrieval prompt, search+coding agents, LangGraph DeepSearch, self-correction prompt.

CoT prompt: "Analyze query -> formulate KB search queries -> gather -> synthesize" with key entities/keywords extracted first.

Agent pair: `SearchAgent(tools=[google_search])` + `CodeAgent(tools=[BuiltInCodeExecutor])` under `gemini-2.0-flash`, composed via `agent_tool`.

DeepSearch graph (`StateGraph`): nodes `generate_query -> web_research -> reflection -> finalize_answer`, entry `START -> generate_query`, conditional edges back to research until reflection passes.

Self-correction prompt: "review content vs original requirements; list gaps; refine for accuracy/completeness/engagement" — run once, diff, keep winner.

## Notebook extracts (on-demand detail)

### Chapter_17_Reasoning_(CoT_Prompt).ipynb

```python
You are an Information Retrieval Agent. Your goal is to answer the user's question comprehensively and accurately by thinking step-by-step.
```

### Chapter_17_Reasoning_(Executing_Code).ipynb

```python
search_agent = Agent(
instruction="""
coding_agent = Agent(
instruction="""
root_agent = Agent(
tools=[agent_tool.AgentTool(agent=search_agent), agent_tool.AgentTool(agent=coding_agent)],
from google.adk.tools import agent_tool
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor
```

### Chapter_17_Reasoning_(Google_DeepSearch).ipynb

```python
"reflection", evaluate_research, ["web_research", "finalize_answer"]
# This means that this node is the first one called
# Add conditional edge to continue with search queries in a parallel branch
```

### Chapter_17_Reasoning_(Self_Correction).ipynb

```python
**Original Prompt/Requirements:** "Write a short, engaging social media post (max 150 characters) announcing a new eco-friendly product line: 'GreenTech Gadgets'."
You are a highly critical and detail-oriented Self-Correction Agent. Your task is to review a previously generated piece of content against its original requirements and identify areas for improvement. Your goal is to refine the content to be more accurate, comprehensive, engaging, and aligned with the prompt.
```
