---
name: exception-handling
description: Detect, handle and recover from tool and system failures. Wrap tool calls and steps with detection, retry, fallback and escalation so a failure degrades gracefully. Do not retry non-transient errors (bad input, insufficient funds) or hide failures from the final response.
role: [safety]
chapter: 12
token_cost_estimate: 340
chains_with: [human-in-the-loop, tool-use, guardrails]
---

# Exception Handling and Recovery

## When to use
- Tools call networks, DBs or external APIs.
- A cheaper fallback exists (general area vs. precise address).
- Batch work should skip bad items, not halt.
- Failures must be logged and reported.

## When NOT to use
- Error is deterministic; retry wastes budget.
- Failure needs a human decision: use `human-in-the-loop`.
- Input is malicious rather than broken: use `guardrails`.

## Inputs
- Primary action
- Fallback action
- Failure flag in state
- Retry/timeout policy

## Outputs
- Result or degraded result
- Error log
- Escalation signal

## Failure modes
- Fallback runs even when primary succeeded (state flag not checked).
- Retrying the same invalid call in a loop.
- Swallowed exception; user sees a confident wrong answer.
- Response agent has no branch for 'nothing retrieved'.

## Minimal example
```python
primary  = Agent(name="primary", tools=[get_precise_location])  # sets state flag on fail
fallback = Agent(name="fallback", instruction="If state['primary_failed']: use get_general_area")
respond  = Agent(name="respond", instruction="Present state['location_result'] or apologise")
robust = SequentialAgent(sub_agents=[primary, fallback, respond])
# tools: raise ValueError on bad input; return error dict only for expected conditions
```

## Next skills
- If recovery needs a human decision: load `human-in-the-loop`
- If the failing unit is a tool: load `tool-use`
- If failure is a policy violation: load `guardrails`
