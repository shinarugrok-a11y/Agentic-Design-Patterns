---
name: multi-agent
description: Specialized agents cooperating via handoff, parallel, loop, or hierarchy. Use when one agent cannot cover the task. Do NOT use for a single specialist.
role: [planner, executor]
chapter: 7
token_cost_estimate: 258
chains_with: [a2a, routing]
---

# Multi-Agent Collaboration

## When to use
- Task needs distinct skills/tools no single agent has
- Sequential handoff, parallel specialists, debate, or coordinator+tools
- Software, research, or creative pipelines with stages

## When NOT to use
- One agent + tools is enough (load `tool-use`)
- Agents live in different processes/frameworks (load `a2a`)
- You only need a classifier, not a team (load `routing`)

## Inputs
- Role instructions and tools
- Topology: Sequential / Parallel / Loop / AgentTool
- State keys (`output_key`) for handoff

## Outputs
- Pipeline result
- Per-role artifacts in session state

## Failure modes
- Coordinator skips delegation
- Loop has no `escalate` / max_iterations
- Parallel writers clobber the same key

## Minimal example
```python
step1 = Agent(name="Fetch", output_key="data")
step2 = Agent(name="Process", instruction="Analyze state['data']")
pipeline = SequentialAgent(sub_agents=[step1, step2])
```

## Next skills
- If specialists are remote/other stacks: load `a2a`
- If a coordinator only triages: load `routing`
