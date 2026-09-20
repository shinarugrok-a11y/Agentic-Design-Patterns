---
name: planning
description: Goal decomposition into ordered executable steps. Decompose a high-level goal into an ordered, dependency-aware list of executable steps before acting. Skip it when one tool call or a known fixed procedure completes the request.
role: [planner]
chapter: 6
token_cost_estimate: 370
chains_with: [goal-setting-and-monitoring, multi-agent-collaboration, prioritization]
---

# Planning

## When to use
- Goal needs multiple interdependent steps
- Steps must be ordered by dependency
- Work spans several tools or agents

## When NOT to use
- One tool call completes the request
- A known fixed procedure already applies
- The environment changes faster than you can plan

## Inputs
- goal statement
- constraints and budget
- available tools and agents

## Outputs
- ordered step list with dependencies
- success criteria per step
- replan trigger conditions

## Failure modes
- Over-planning trivial tasks wastes tokens and time
- Plan assumes tools or data that do not exist
- No replanning hook, so the agent follows a stale plan
- Steps too coarse for an executor to act on

## Minimal example
```python
plan = llm.invoke(PLAN_PROMPT.format(goal=goal, tools=tool_names))
# [{"id":1,"action":"search","depends_on":[],"done_when":"3 sources found"}, ...]
for step in topological_order(plan):
    result = execute(step)
    if not meets(step["done_when"], result):
        plan = replan(goal, done=results, failure=step)
```

## Next skills
- If success must be tracked: load `goal-setting-and-monitoring`
- If steps need specialists: load `multi-agent-collaboration`
- If steps compete for resources: load `prioritization`
