# Planning — deep dive

Source: Chapter 6 + `Chapter_06_Planning_(Code_Example).ipynb`,
`Chapter_06_Planning_(Deep_Research_API).ipynb`.
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

## Rule of thumb (SOURCE, GT:L4220–L4224)
Use when a request is too complex for a single action or tool: multi-step
processes such as producing a research report, onboarding an employee, or a
competitive analysis. That planning makes an agent strategic and adaptive is
the chapter's framing (DERIVED wording).

## Pattern A: plan-then-write in one CrewAI task
Provenance: SOURCE (abridged) — condensed from GT:L3884–L3921; not verbatim.
```python
from crewai import Agent, Task, Crew, Process

planner_writer_agent = Agent(
    role="Article Planner and Writer",
    goal="Plan and then write a concise, engaging summary on a specified topic.",
    backstory=("You are an expert technical writer and content strategist. "
               "Your strength lies in creating a clear, actionable plan before writing, "
               "ensuring the final summary is both informative and easy to digest."),
    allow_delegation=False, llm=llm)

topic = "The importance of Reinforcement Learning in AI"
high_level_task = Task(
    description=(f"1. Create a bullet-point plan for a summary on the topic: '{topic}'.\n"
                 f"2. Write the summary based on your plan, keeping it around 200 words."),
    expected_output=("A final report containing two distinct sections:\n\n"
                     "### Plan\n- A bulleted list outlining the main points of the summary.\n\n"
                     "### Summary\n- A concise and well-structured summary of the topic."),
    agent=planner_writer_agent)

Crew(agents=[planner_writer_agent], tasks=[high_level_task], process=Process.sequential).kickoff()
```
The trick is in `expected_output`: demanding a visible `### Plan` section
forces the model to plan before it writes.

## Pattern B: delegated planning agent (OpenAI Deep Research)
Provenance: SOURCE (abridged) — condensed from GT:L4098–L4175 (`Chapter_06_Planning_(Deep_Research_API).ipynb`); loops and prints removed. `o3-deep-research-2025-06-26` is time-specific (UNCERTAIN today).
```python
response = client.responses.create(
    model="o3-deep-research-2025-06-26",
    input=[{"role": "developer", "content": [{"type": "input_text", "text":
            "You are a professional researcher preparing a structured, data-driven report. "
            "Focus on data-rich insights, use reliable sources, and include inline citations."}]},
           {"role": "user", "content": [{"type": "input_text", "text":
            "Research the economic impact of semaglutide on global healthcare systems."}]}],
    reasoning={"summary": "auto"},
    tools=[{"type": "web_search_preview"}])

final_report = response.output[-1].content[0].text
annotations = response.output[-1].content[0].annotations   # citations with start/end index, title, url
reasoning_step = next(i for i in response.output if i.type == "reasoning")        # the plan
search_step = next(i for i in response.output if i.type == "web_search_call")     # executed queries
code_step = next(i for i in response.output if i.type == "code_interpreter_call") # code run
```
Deep Research plans, searches, reflects and revises internally; you inspect
the trajectory through the typed items in `response.output`.

## Plan prompt template (explicit planner)
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
Goal: {goal}
Available tools: {tools}
Constraints: {constraints}
Produce a numbered plan. For each step give: id, action, tool (or none),
inputs (reference earlier step ids), success check. Max {n} steps.
Return JSON: {"steps": [...]}
```
Re-plan prompt:
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
Plan: {plan}
Completed: {done}
Failure at step {k}: {error}
Revise the remaining steps. Keep completed steps unchanged.
```

## Execution loop sketch
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```python
plan = plan_llm(goal, tools)
for step in plan.steps:
    result = execute(step)              # tool-use / sub-agent / prompt-chaining
    state[step.id] = result
    if not step.success_check(result):
        plan = replan_llm(plan, state, step, result)
```

## When planning is overkill (DERIVED)
- Single tool call answers the request.
- The pipeline is fixed: encode it directly with `prompt-chaining`.
- Token budget is tiny; planning tokens exceed the work.

## Related book concepts (SOURCE, GT:L3987–L4031, figures only, no code)
Google Deep Research: iterative research plans that adapt as information
is gathered (plan -> search -> reflect -> re-plan). See `reasoning-techniques`
for the reflection graph.

## Pattern variants (DERIVED summary; book terms cited where present)
- **Plan-then-execute** — one agent emits the plan as its first output, then works it; wins when the "how" must be discovered but the steps are stable once chosen.
- **Fixed workflow (no planning)** — hard-code the step order when the solution is already well-understood; wins whenever predictability beats flexibility.
- **Adaptive replanning** — treat the first plan as a starting point and re-derive it when a step's constraint fails (venue unavailable, source missing); wins in dynamic environments.
- **Delegated deep research** — hand the goal to a research model that decomposes into sub-questions, searches, and returns a cited report; wins for broad synthesis over many sources.

## More prompt templates
Force the plan to be a visible artifact, not hidden reasoning:

Provenance: SOURCE (abridged) — task description + expected output from GT:L3910–L3925, reflowed.
```
1. Create a bullet-point plan for a summary on the topic: '{topic}'.
2. Write the summary based on your plan, keeping it around 200 words.

Expected output — a final report with two distinct sections, "### Plan"
(a bulleted list of the main points) then "### Summary".
```

Machine-checkable plan, so each step can be validated before execution:

Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
Goal: {goal}
Tools available: {tool_names}
Return JSON only: a list of steps, each with
  "id", "action" (must name one of the tools above),
  "depends_on" (list of ids), "done_when" (an observable success test).
Do not include a step whose action is not in the tool list.
```

Research-agent persona:

Provenance: SOURCE — lines found verbatim in GT:L4094–L4096.
```
You are a professional researcher preparing a structured, data-driven report.
Focus on data-rich insights, use reliable sources, and include inline citations.
```

## Framework notes
- **LangChain / LangGraph** — present only as the model binding (`ChatOpenAI`) given to the planning agent.
- **Google ADK** — no ADK planner in this chapter; Google Deep Research is described with screenshots only (GT:L3987–L4031).
- **CrewAI** — `Agent` + `Task` + `Process.sequential`; the plan is produced by prompt shape (`description` / `expected_output`), not by a dedicated planner class.

## Failure modes in depth (DERIVED)
- **Over-planning trivial tasks** — planning is a tool, not a default. If the "how" is already known, use a fixed workflow; the cost is tokens, latency, and unpredictable behavior.
- **Plan assumes tools or data that do not exist** — pass the real tool registry into the plan prompt and reject any step whose `action` is not in it before execution begins.
- **No replanning hook** — check each step's `done_when` against the actual result and call `replan(goal, done, failure)` on mismatch, instead of running the remaining steps against a stale world.
- **Steps too coarse for an executor** — require each step to name one tool call and one observable success test; split any step that needs both.
