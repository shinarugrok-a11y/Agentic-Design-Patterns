# Reasoning Techniques — reference patterns

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
