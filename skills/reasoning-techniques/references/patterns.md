# Reasoning Techniques — Pattern reference

Load this file only when implementing `reasoning-techniques`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when the problem needs explicit multi-step inference (CoT, ToT, ReAct, self-correction) rather than a single completion.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: CoT prompt + step-by-step. Fig. 2: Tree of Thoughts. Fig. 3: ReAct. Fig. 7: Reasoning design pattern.

## Notebooks (extracted)

Reasoning Techniques

### Notebooks
- `Chapter_17_Reasoning_(CoT_Prompt).ipynb` *(prompt text + worked example, not Python)*
- `Chapter_17_Reasoning_(Executing_Code).ipynb`
- `Chapter_17_Reasoning_(Google_DeepSearch).ipynb` *(LangGraph fragment)*
- `Chapter_17_Reasoning_(Self_Correction).ipynb` *(prompt text + worked example)*

### Patterns
- **CoT prompt engineering:** 5-step process (analyze → search queries → simulate retrieval → synthesize → review)
- **Self-correction prompt:** compare output to requirements → identify weaknesses → propose fixes → rewrite
- **Multi-agent reasoning:** root agent with `AgentTool` wrapping search + code execution specialists
- **DeepSearch graph:** cyclic web_research ↔ reflection until ready to finalize

### Prompt templates
CoT agent opener:
```
You are an Information Retrieval Agent. Your goal is to answer the user's question comprehensively and accurately by thinking step-by-step.

Here's the process you must follow:

1.  **Analyze the Query:** Understand the core subject and specific requirements of the user's question.
2.  **Formulate Search Queries (for Knowledge Base):** Based on your analysis, generate a list of precise search queries...
3.  **Simulate Information Retrieval (Self-Correction/Reasoning):** For each search query, mentally consider what kind of information you expect to find.
4.  **Synthesize Information:** Based on the simulated retrieval... synthesize the gathered information into a coherent and complete answer.
5.  **Review and Refine:** Before finalizing, critically evaluate your answer.
```

Self-correction opener:
```
You are a highly critical and detail-oriented Self-Correction Agent. Your task is to review a previously generated piece of content against its original requirements and identify areas for improvement.
...
5.  **Generate Revised Content:** Based on your proposed improvements, rewrite the original content...
```

### Minimal code
```python
# Multi-agent reasoning (ADK)
search_agent = Agent(name='SearchAgent', tools=[google_search], instruction="You're a specialist in Google Search")
coding_agent = Agent(name='CodeAgent', code_executor=[BuiltInCodeExecutor], instruction="You're a specialist in Code Execution")
root_agent = Agent(
    name="RootAgent",
    tools=[agent_tool.AgentTool(agent=search_agent), agent_tool.AgentTool(agent=coding_agent)],
)
```

```python
# DeepSearch graph (fragment)
builder.add_conditional_edges("generate_query", continue_to_web_research, ["web_research"])
builder.add_conditional_edges("reflection", evaluate_research, ["web_research", "finalize_answer"])
graph = builder.compile(name="pro-search-agent")
```

### Caveats
- CoT and Self_Correction notebooks are **prompt documents** with worked examples — not executable Python
- DeepSearch notebook is graph wiring only — node functions not included
- Executing_Code notebook uses `code_executor=[BuiltInCodeExecutor]` (list form) — verify against current ADK API

---

## Failure modes (skill-level)
- Fake CoT that does not constrain the answer
- DeepSearch graph with missing node functions
- Unbounded reflect↔search cycles

## Chains with
`reflection`, `planning`
