---
name: multi-agent-collaboration
description: Cooperating specialized agents. Split a multi-domain goal across specialized agents coordinated by handoff, hierarchy, or debate. Skip it when one agent with the right tools already solves the task.
role: [planner, executor]
chapter: 7
token_cost_estimate: 380
chains_with: [planning, inter-agent-communication-a2a, parallelization]
---

# Multi-Agent Collaboration

## When to use
- Subtasks need different tools or expertise
- Work splits into distinct roles or stages
- Peer review or debate improves the result

## When NOT to use
- One agent with the right tools suffices
- Coordination overhead outweighs specialization
- Handoff would lose context the task depends on

## Inputs
- decomposed subtasks
- agent roles and tools
- coordination topology

## Outputs
- per-agent results
- coordinator synthesis
- handoff transcript

## Failure modes
- Coordination overhead exceeds the benefit of specialization
- Agents duplicate work or deadlock waiting on each other
- Context is lost or distorted at each handoff
- Errors compound across agents with no shared critic

## Minimal example
```python
coordinator = LlmAgent(
    name="coordinator",
    instruction="Delegate to researcher, then analyst, then writer.",
    sub_agents=[researcher, analyst, writer],   # sequential handoff
)
```

## Next skills
- If roles need a plan first: load `planning`
- If agents are cross-framework: load `inter-agent-communication-a2a`
- If roles are independent: load `parallelization`
