# Planning — Patterns

## Pattern variants
- **Plan-then-execute** — one agent emits the plan as its first output, then works it; wins when the "how" must be discovered but the steps are stable once chosen.
- **Fixed workflow (no planning)** — hard-code the step order when the solution is already well-understood; wins whenever predictability beats flexibility.
- **Adaptive replanning** — treat the first plan as a starting point and re-derive it when a step's constraint fails (venue unavailable, source missing); wins in dynamic environments.
- **Delegated deep research** — hand the goal to a research model that decomposes into sub-questions, searches, and returns a cited report; wins for broad synthesis over many sources.

## Prompt templates
Force the plan to be a visible artifact, not hidden reasoning:

```
1. Create a bullet-point plan for a summary on the topic: '{topic}'.
2. Write the summary based on your plan, keeping it around 200 words.

Expected output — a final report with two distinct sections, "### Plan"
(a bulleted list of the main points) then "### Summary".
```

Machine-checkable plan, so each step can be validated before execution:

```
Goal: {goal}
Tools available: {tool_names}
Return JSON only: a list of steps, each with
  "id", "action" (must name one of the tools above),
  "depends_on" (list of ids), "done_when" (an observable success test).
Do not include a step whose action is not in the tool list.
```

Research-agent persona:

```
You are a professional researcher preparing a structured, data-driven report.
Focus on data-rich insights, use reliable sources, and include inline citations.
```

## Code patterns
CrewAI (plan and execution as one task, run sequentially):

```python
high_level_task = Task(
    description=(f"1. Create a bullet-point plan for a summary on: '{topic}'.\n"
                 f"2. Write the summary based on your plan, around 200 words."),
    expected_output="A report with a '### Plan' section then a '### Summary' section.",
    agent=planner_writer_agent,
)
crew = Crew(agents=[planner_writer_agent], tasks=[high_level_task],
            process=Process.sequential)
result = crew.kickoff()
```

OpenAI Deep Research (planning delegated to the model; steps are inspectable):

```python
response = client.responses.create(
    model="o3-deep-research-2025-06-26",
    input=[{"role": "developer", "content": [{"type": "input_text", "text": system_message}]},
           {"role": "user", "content": [{"type": "input_text", "text": user_query}]}],
    reasoning={"summary": "auto"},
    tools=[{"type": "web_search_preview"}],
)
plan_step = next(i for i in response.output if i.type == "reasoning")
search_step = next(i for i in response.output if i.type == "web_search_call")
```

## Framework notes
- **LangChain / LangGraph** — present only as the model binding (`ChatOpenAI`) given to the planning agent.
- **Google ADK** — no ADK planner here; the chapter uses Gemini Deep Research, which plans, searches, reflects on gaps, and replans asynchronously.
- **CrewAI** — `Agent` + `Task` + `Process.sequential`; the plan is produced by prompt shape (`description` / `expected_output`), not by a dedicated planner class.

## Failure modes in depth
- **Over-planning trivial tasks** — planning is a tool, not a default. If the "how" is already known, use a fixed workflow; the cost is tokens, latency, and unpredictable behavior.
- **Plan assumes tools or data that do not exist** — pass the real tool registry into the plan prompt and reject any step whose `action` is not in it before execution begins.
- **No replanning hook** — check each step's `done_when` against the actual result and call `replan(goal, done, failure)` on mismatch, instead of running the remaining steps against a stale world.
- **Steps too coarse for an executor** — require each step to name one tool call and one observable success test; split any step that needs both.

## Source
Chapter 6 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_06_Planning_(Code_Example).ipynb, Chapter_06_Planning_(Deep_Research_API).ipynb.
