# Planning — Pattern reference

Load this file only when implementing `planning`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when a request needs a sequence of interdependent operations, not a single tool call.

## Book — visual (figure captions; images stay in the PDF)
Fig. 4: Planning design pattern. Also: Deep Research plan → search execution → synthesized report.

## Notebooks (extracted)

Planning

### Notebooks
- `Chapter_06_Planning_(Code_Example).ipynb`
- `Chapter_06_Planning_(Deep_Research_API).ipynb`

### Patterns
- **CrewAI:** single agent, single task with two-step description (plan bullets → write summary); `Process.sequential`
- **OpenAI Deep Research:** `client.responses.create` with `o3-deep-research`, `web_search_preview` tool, reasoning summary
- **Structured output:** task `expected_output` defines `### Plan` and `### Summary` sections

### Prompt templates
Deep Research system message:
```
You are a professional researcher preparing a structured, data-driven report.
Focus on data-rich insights, use reliable sources, and include inline citations.
```

CrewAI task description pattern:
```
1. Create a bullet-point plan for a summary on the topic: '{topic}'.
2. Write the summary based on your plan, keeping it around 200 words.
```

### Minimal code
```python
# CrewAI plan-then-write
planner = Agent(role='Article Planner and Writer', goal='Plan and write a concise summary.', llm=llm)
task = Task(
    description="1. Create a bullet-point plan...\n2. Write the summary...",
    expected_output="### Plan\n...\n### Summary\n...",
    agent=planner,
)
result = Crew(agents=[planner], tasks=[task], process=Process.sequential).kickoff()
```

```python
# OpenAI Deep Research (fragment)
response = client.responses.create(
    model="o3-deep-research-2025-06-26",
    input=[{"role": "developer", "content": [{"type": "input_text", "text": system_message}]},
           {"role": "user", "content": [{"type": "input_text", "text": user_query}]}],
    reasoning={"summary": "auto"},
    tools=[{"type": "web_search_preview"}],
)
```

### Caveats
- Deep Research requires OpenAI API access to research models
- Inspect `response.output` for reasoning, web_search_call, code_interpreter_call steps
- CrewAI uses `gpt-4-turbo` — assign explicit `llm` to agent

---

## Failure modes (skill-level)
- Plan never executed (plan-only stall)
- Steps ignore tool constraints
- No replanning when a step fails

## Chains with
`goal-setting`, `tool-use`
