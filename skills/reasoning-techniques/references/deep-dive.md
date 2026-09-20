# Reasoning Techniques — deep dive

Source: Chapter 17 + `Chapter_17_Reasoning_(CoT_Prompt)`, `(Self_Correction)`,
`(Executing_Code)`, `(Google_DeepSearch)`.

## Techniques (book)
| Technique | Idea | Cost |
|---|---|---|
| Chain-of-Thought (CoT) | make intermediate steps explicit | + output tokens |
| Tree-of-Thought (ToT) | explore several reasoning branches, evaluate, backtrack | multiplicative |
| Self-Correction | critique own draft against requirements, rewrite | 2-3x |
| ReAct | interleave Thought -> Action (tool) -> Observation | tool calls |
| Chain of Debates (CoD) | several agents argue to reduce individual bias | N agents |
| Program-Aided (PAL) | offload computation to executed code | code executor |
| Scaling Inference Law | more "thinking time" at inference improves quality | latency |
| MASS | automated optimisation of multi-agent prompts and topology | offline |

Rule of thumb: use when a problem needs decomposition, multi-step logic,
tool interaction or strategic adaptation, and when the visible "work"
matters as much as the answer.

## CoT prompt (Information Retrieval Agent)
```
You are an Information Retrieval Agent. Your goal is to answer the user's question comprehensively and accurately by thinking step-by-step.

Here's the process you must follow:
1.  **Analyze the Query:** Understand the core subject and specific requirements. Identify key entities, keywords, and the type of information being sought.
2.  **Formulate Search Queries (for Knowledge Base):** Generate a list of precise search queries.
3.  **Simulate Information Retrieval (Self-Correction/Reasoning):** For each query, consider what you expect to find and the most relevant snippets. Think about ambiguities or missing pieces.
4.  **Synthesize Information:** Combine into a coherent, complete answer addressing all aspects.
5.  **Review and Refine:** Is it accurate? comprehensive? clear? concise? If not, identify what to improve.

**User Query:** "{query}"
```
The notebook shows the model emitting `Thought 1..5` then a final answer;
keep the thoughts and answer in clearly labelled sections so callers can
strip the trace.

## Self-Correction prompt
```
You are a highly critical and detail-oriented Self-Correction Agent. Review a previously generated piece of content against its original requirements and identify areas for improvement.

1.  **Understand Original Requirements:** original intent, key constraints, goals.
2.  **Analyze Current Content.**
3.  **Identify Discrepancies/Weaknesses:** Accuracy, Completeness, Clarity & Coherence, Tone & Style, Engagement, Redundancy/Verbosity.
4.  **Propose Specific Improvements:** concrete, actionable changes; propose a solution, not just the problem.
5.  **Generate Revised Content:** polished and ready for use.

**Original Prompt/Requirements:** "{requirements}"
**Initial Draft:** "{draft}"
```
Example from the notebook: 150-char social post; the draft "We have new
products. They are green and techy..." is rewritten into a 148-char post
that names the eco benefit, adds a CTA and hashtags.

## ReAct-style research graph (LangGraph, Google DeepSearch)
```python
builder = StateGraph(OverallState, config_schema=Configuration)
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("reflection", reflection)
builder.add_node("finalize_answer", finalize_answer)
builder.add_edge(START, "generate_query")
builder.add_conditional_edges("generate_query", continue_to_web_research, ["web_research"])  # parallel fan-out
builder.add_edge("web_research", "reflection")
builder.add_conditional_edges("reflection", evaluate_research, ["web_research", "finalize_answer"])  # loop or finish
builder.add_edge("finalize_answer", END)
graph = builder.compile(name="pro-search-agent")
```
`reflection` decides whether knowledge gaps remain (loop) or the answer is
sufficient (finalize). Bound the loop with an iteration counter in state.

## Program-aided reasoning (ADK agents as tools)
```python
search_agent = Agent(model="gemini-2.0-flash", name="SearchAgent",
    instruction="You're a specialist in Google Search", tools=[google_search])
coding_agent = Agent(model="gemini-2.0-flash", name="CodeAgent",
    instruction="You're a specialist in Code Execution", code_executor=[BuiltInCodeExecutor])
root_agent = Agent(name="RootAgent", model="gemini-2.0-flash", description="Root Agent",
    tools=[agent_tool.AgentTool(agent=search_agent), agent_tool.AgentTool(agent=coding_agent)])
```
Route arithmetic/data work to the code agent instead of reasoning in text.

## Choosing a technique
- Single answer, moderate difficulty -> CoT.
- Need tools/facts -> ReAct (or the research graph).
- Draft exists, must meet spec -> Self-Correction (see `reflection`).
- Several plausible strategies -> ToT with an evaluator and a branch cap.
- Numeric/precise -> code execution.
- High-stakes judgment -> CoD with distinct personas, then arbitrate.

## Pitfalls
- Reasoning traces leak into user-facing output; separate sections.
- Extra tokens on trivial tasks; gate by `resource-aware-optimization`.
- Models with built-in hidden reasoning may not need explicit CoT; test both.

## Pattern variants
- **Chain-of-Thought (CoT)** — one linear sequence of intermediate steps; cheapest, enough when the path does not branch.
- **Tree-of-Thoughts (ToT)** — branch into candidate thoughts, evaluate, backtrack; wins when the first plausible path is often wrong.
- **Self-correction / self-refinement** — critique the draft against the original requirements, then rewrite; wins where a quality bar, not a fact, is the hard part.
- **ReAct** — interleave Thought, Action, Observation so feedback steers the next step; the default once tools or external state are involved.
- **Program-Aided Language Models (PALM)** — offload arithmetic, symbolic, or data work to generated code, executed deterministically.
- **Self-consistency / multiple candidates** — sample several answers and select one; the Scaling Inference Law in practice, where a small model with a big thinking budget beats a larger one-pass model.
- **Chain of Debates (CoD), Deep Research** — several diverse models argue to cut single-model bias; or one agent loops search, reflect on gaps, re-search, synthesize under a time budget.

## More prompt templates
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

## Framework notes
- **LangChain / LangGraph** — cycles are the point: `add_conditional_edges` from a reflection node back to research turns a chain into deliberation; the loop cap lives in graph config.
- **Google ADK** — `BuiltInCodeExecutor` for PALM-style execution; `agent_tool.AgentTool` exposes a reasoning specialist as a callable tool of a root agent.

## Failure modes in depth
- **Fluent but wrong traces** — a trace is generated text, not proof, and can rationalize a wrong answer; verify the conclusion independently (code execution, retrieval, a critic pass).
- **Combinatorial tree explosion** — ToT branching with no evaluator; score each thought, keep top-k, cap depth and total node budget.
- **ReAct repeating a failed action** — the observation never changes, so neither does the next thought; cap steps, hash (action, args) to detect repeats, and force a different action or a final answer.
- **Traces leaked to users** — reasoning carries retrieved internal data and half-formed conclusions; return the answer plus a short justification, keep the full trace in logs.
