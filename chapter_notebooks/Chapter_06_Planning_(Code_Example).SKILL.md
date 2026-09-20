---
name: planning
description: Decompose a goal into ordered steps before acting. Use for multi-step objectives. Do NOT use for single-tool requests.
role: [planner]
chapter: 6
token_cost_estimate: 256
chains_with: [goal-setting, tool-use]
---

# Planning

## When to use
- Goal needs several interdependent operations
- Research reports, onboarding, competitive analysis
- Must show a plan (bullets) then produce the artifact

## When NOT to use
- Single tool/prompt is enough (load `tool-use`)
- Work is independent fan-out (load `parallelization`)
- Success is a SMART target to monitor (also load `goal-setting`)

## Inputs
- High-level objective
- Tool/agent inventory
- Expected plan + summary schema

## Outputs
- Ordered plan (sub-goals)
- Executed artifact with optional citations

## Failure modes
- Emits a plan and stops
- Steps name tools that do not exist
- Failure in step k with no replan

## Minimal example
```python
task = Task(description="1. Bullet plan for {topic}\n2. Write ~200-word summary",
            expected_output="### Plan\n...\n### Summary\n...")
Crew(agents=[planner], tasks=[task], process=Process.sequential).kickoff()
```

## Next skills
- If you must know when the goal is met: load `goal-setting`
- If steps are tool calls: load `tool-use`
