# Parallelization — Patterns

## Pattern variants
- **Map-then-synthesize** — fan out N prompts over the same input, then feed all branch outputs into one synthesis prompt; wins for multi-faceted analysis of a single topic.
- **Multi-source gather** — each branch hits a different API, index, or database; wins when latency is dominated by I/O wait.
- **Sectioning** — split one artifact into independent sections (or a batch into chunks) and generate each concurrently; wins for long content assembled from separable parts.
- **Parallel sub-agents with a merger** — branches are full agents writing to shared state, followed by a dedicated synthesis agent; wins when branches need distinct tools or instructions.
- **LLM-driven delegation** — a coordinator's LLM recognises that sub-tasks are independent and triggers them concurrently; wins when the fan-out set is not known statically.

## Prompt templates

Branch prompts stay narrow and fixed-format so the aggregator can rely on shape:

```text
Summarize the following topic concisely:
{topic}
---
Generate three interesting questions about the following topic:
{topic}
---
Identify 5-10 key terms from the following topic, separated by commas:
{topic}
```

Aggregator prompt — name each branch and forbid outside knowledge:

```text
You are responsible for combining research findings into a structured report.
Synthesize the following summaries, clearly attributing findings to their
source areas.

Crucially: your entire response MUST be grounded *exclusively* on the
information provided in the Input Summaries below. Do NOT add external
knowledge or details not present in these summaries.

*   Renewable Energy: {renewable_energy_result}
*   Electric Vehicles: {ev_technology_result}
*   Carbon Capture:    {carbon_capture_result}
```

## Code patterns

LangChain (LCEL, `RunnableParallel`):

```python
map_chain = RunnableParallel({
    "summary": summarize_chain,
    "questions": questions_chain,
    "key_terms": terms_chain,
    "topic": RunnablePassthrough(),     # carry the original input to synthesis
})

full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()
await full_parallel_chain.ainvoke(topic)
```

Google ADK (`ParallelAgent` + merger):

```python
parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
)
# Each researcher declares output_key="..."; the merger's instruction
# interpolates those session.state keys and runs after the join.
```

## Framework notes
- **LangChain / LangGraph** — `RunnableParallel` (or a plain dict literal in LCEL) runs branches side by side; use `ainvoke`/`abatch` so the concurrency is real, and `asyncio.gather` directly when branches are not Runnables.
- **Google ADK** — `ParallelAgent` joins only after every sub-agent finishes; branches communicate solely through `output_key` writes into `session.state`.

## Failure modes in depth
- **Hidden dependency between branches** — a branch silently relies on another's output and reads stale or empty state. Assert each branch's inputs come only from the shared input, and move any true dependency into a sequential step after the join.
- **Rate limits from burst fan-out** — N simultaneous calls trip quota and return 429s. Cap concurrency with a semaphore or batch size and back off per branch rather than per request.
- **Aggregator starved by one failure** — an unhandled branch exception aborts the join and the synthesis never runs. Use `asyncio.gather(..., return_exceptions=True)`, drop failed branches, and tell the aggregator which sources are missing.
- **Interleaved logs** — concurrent branches emit a scrambled trace. Tag every log line with the branch or `output_key` name and buffer branch output until it completes.

## Source
Chapter 3 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_03_Parallelization_(Google_ADK).ipynb, Chapter_03_Parallelization_(LangChain).ipynb.
