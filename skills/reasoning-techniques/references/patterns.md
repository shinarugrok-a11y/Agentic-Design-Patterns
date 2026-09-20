# Reasoning Techniques — Patterns

## Pattern variants
- **Chain-of-Thought (CoT)** — one linear sequence of intermediate steps; cheapest, enough when the path does not branch.
- **Tree-of-Thoughts (ToT)** — branch into candidate thoughts, evaluate, backtrack; wins when the first plausible path is often wrong.
- **Self-correction / self-refinement** — critique the draft against the original requirements, then rewrite; wins where a quality bar, not a fact, is the hard part.
- **ReAct** — interleave Thought, Action, Observation so feedback steers the next step; the default once tools or external state are involved.
- **Program-Aided Language Models (PALM)** — offload arithmetic, symbolic, or data work to generated code, executed deterministically.
- **Self-consistency / multiple candidates** — sample several answers and select one; the Scaling Inference Law in practice, where a small model with a big thinking budget beats a larger one-pass model.
- **Chain of Debates (CoD), Deep Research** — several diverse models argue to cut single-model bias; or one agent loops search, reflect on gaps, re-search, synthesize under a time budget.

## Prompt templates

CoT, numbered stages (the chapter's retrieval agent):
```
Answer the question by thinking step-by-step.
1. Analyze the query: key entities and what is actually being asked.
2. Formulate the search queries you would run against the knowledge base.
3. Simulate retrieval: what would each return, what stays ambiguous?
4. Synthesize the findings into a complete answer.
5. Review and refine: accurate, comprehensive, concise? If not, fix it.
Query: {question}
```

Self-correction over an existing draft:
```
You are a critical, detail-oriented Self-Correction Agent.
1. Restate the original requirements and constraints.
2. Name every discrepancy: accuracy, completeness, clarity, tone, redundancy.
3. Propose a concrete fix for each — a solution, not just the problem.
4. Output the fully revised content.
Requirements: {requirements}
Draft: {draft}
```

## Code patterns

Google ADK (code execution and search wrapped as sub-agent tools):
```python
coding_agent = Agent(model='gemini-2.0-flash', name='CodeAgent',
                     instruction="You're a specialist in Code Execution",
                     code_executor=[BuiltInCodeExecutor])
root_agent = Agent(name="RootAgent", model="gemini-2.0-flash",
                   tools=[agent_tool.AgentTool(agent=search_agent),
                          agent_tool.AgentTool(agent=coding_agent)])
```

LangGraph (Deep Research: the reflection node decides whether to loop or finish):
```python
builder = StateGraph(OverallState, config_schema=Configuration)
builder.add_edge(START, "generate_query")
builder.add_conditional_edges("generate_query", continue_to_web_research,
                              ["web_research"])        # fan out in parallel
builder.add_edge("web_research", "reflection")
builder.add_conditional_edges("reflection", evaluate_research,
                              ["web_research", "finalize_answer"])  # loop or stop
graph = builder.compile(name="pro-search-agent")
```

## Framework notes
- **LangChain / LangGraph** — cycles are the point: `add_conditional_edges` from a reflection node back to research turns a chain into deliberation; the loop cap lives in graph config.
- **Google ADK** — `BuiltInCodeExecutor` for PALM-style execution; `agent_tool.AgentTool` exposes a reasoning specialist as a callable tool of a root agent.

## Failure modes in depth
- **Fluent but wrong traces** — a trace is generated text, not proof, and can rationalize a wrong answer; verify the conclusion independently (code execution, retrieval, a critic pass).
- **Combinatorial tree explosion** — ToT branching with no evaluator; score each thought, keep top-k, cap depth and total node budget.
- **ReAct repeating a failed action** — the observation never changes, so neither does the next thought; cap steps, hash (action, args) to detect repeats, and force a different action or a final answer.
- **Traces leaked to users** — reasoning carries retrieved internal data and half-formed conclusions; return the answer plus a short justification, keep the full trace in logs.

## Source
Chapter 17 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_17_Reasoning_(CoT_Prompt).ipynb, Chapter_17_Reasoning_(Self_Correction).ipynb, Chapter_17_Reasoning_(Executing_Code).ipynb, Chapter_17_Reasoning_(Google_DeepSearch).ipynb.
