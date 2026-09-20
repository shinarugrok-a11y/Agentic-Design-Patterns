---
name: multi-agent
description: Coordinate specialist agents via sequential, parallel, loop, or coordinator topologies.
role: [planner, executor]
chapter: 7
token_cost_estimate: 218
chains_with: [planning, evaluation-monitoring]
---

# Multi-Agent Collaboration

## When to use
- Subtasks need distinct roles or tools per agent.
- Topology fits: sequential, parallel, loop, or coordinator.
- Agents communicate through defined handoffs, not chaos.

## When NOT to use
- One agent with tools suffices; avoid coordination overhead.
- Shared-state conflicts cannot be arbitrated.

## Inputs
- Role roster + topology
- Handoff protocol between agents

## Outputs
- Combined result + per-agent contributions

## Failure modes
- Unclear ownership; two agents redo or skip work.
- Loop topology never converges without an exit check.
- Message bloat explodes context across agents.

## Minimal example
```python
crew = Crew(agents=[researcher, writer], tasks=[research_t, write_t])
print(crew.kickoff())  # or ADK SequentialAgent/ParallelAgent/LoopAgent
```

## Next skills
- If handoffs need ordering and ownership rules: load `planning`
- If agent outputs need judging: load `evaluation-monitoring`
