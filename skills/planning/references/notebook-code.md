# Planning — reference patterns

Source: Chapter 6 + `Chapter_06_Planning_(Code_Example).ipynb`,
`Chapter_06_Planning_(Deep_Research_API).ipynb`.

## Rule of thumb (book)
Use when a request is too complex for a single action or tool: multi-step
processes such as producing a research report, onboarding an employee, or a
competitive analysis. Planning turns a reactive agent into a strategic
executor that can also adapt its plan.

## Pattern A: plan-then-write in one CrewAI task
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
```
Goal: {goal}
Available tools: {tools}
Constraints: {constraints}
Produce a numbered plan. For each step give: id, action, tool (or none),
inputs (reference earlier step ids), success check. Max {n} steps.
Return JSON: {"steps": [...]}
```
Re-plan prompt:
```
Plan: {plan}
Completed: {done}
Failure at step {k}: {error}
Revise the remaining steps. Keep completed steps unchanged.
```

## Execution loop sketch
```python
plan = plan_llm(goal, tools)
for step in plan.steps:
    result = execute(step)              # tool-use / sub-agent / prompt-chaining
    state[step.id] = result
    if not step.success_check(result):
        plan = replan_llm(plan, state, step, result)
```

## When planning is overkill
- Single tool call answers the request.
- The pipeline is fixed: encode it directly with `prompt-chaining`.
- Token budget is tiny; planning tokens exceed the work.

## Related book concepts
Google Deep Research: iterative research plans that adapt as information
is gathered (plan -> search -> reflect -> re-plan). See `reasoning-techniques`
for the reflection graph.
