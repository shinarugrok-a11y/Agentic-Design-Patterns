---
name: multi-agent
description: Specialised agents cooperating via handoff, parallel, loop or hierarchy. Split a task across specialist agents with their own tools and instructions, coordinated by a defined interaction model. Do not use when one agent with the right tools can finish the task; coordination overhead is real.
role: [planner, executor]
chapter: 7
token_cost_estimate: 340
chains_with: [a2a, routing, parallelization]
---

# Multi-Agent Collaboration

## When to use
- Sub-tasks need different expertise, tools or system prompts.
- Work maps to roles (researcher -> writer -> reviewer).
- Coordinator should delegate rather than answer.
- Loop until a state condition is met (`LoopAgent` + escalate).

## When NOT to use
- Single agent with 2-3 tools suffices.
- Agents are on different frameworks/hosts: use `a2a`.
- Latency budget cannot absorb multiple model calls.

## Inputs
- Role definitions (name, description, instruction, tools)
- Interaction model (sequential | parallel | loop | coordinator)
- Shared state keys

## Outputs
- Composed result
- Per-agent outputs in state
- Delegation trace

## Failure modes
- Coordinator answers itself instead of delegating.
- Ambiguous agent descriptions cause wrong delegation.
- State key naming mismatch between writer and reader agent.
- Loop never sets the exit condition; hits `max_iterations`.

## Minimal example
```python
coordinator = LlmAgent(name="Coordinator", sub_agents=[booker, info],
    instruction="Delegate only. Booking->Booker, else->Info.")
pipeline = SequentialAgent(sub_agents=[fetch(output_key="data"), summarise])
poller = LoopAgent(max_iterations=10, sub_agents=[step, ConditionChecker()])
# ConditionChecker yields Event(actions=EventActions(escalate=True)) to stop
```

## Next skills
- If agents span frameworks or hosts: load `a2a`
- If coordinator logic is pure classification: load `routing`
- If sub-agents are independent: load `parallelization`
