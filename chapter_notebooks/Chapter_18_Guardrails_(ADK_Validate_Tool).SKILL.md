---
name: guardrails
description: Screen inputs, tool args and outputs against policy. Use for any exposed agent. Never rely on one layer.
role: [safety]
chapter: 18
token_cost_estimate: 225
chains_with: [human-in-the-loop, evaluation-monitoring]
---

# Guardrails and Safety

## When to use
- Untrusted input reaches the agent.
- Tools can take dangerous actions.
- Output must meet policy.

## When NOT to use
- Never skip; keep layers cheap for trusted flows.
- Self-policing alone is not a guardrail.

## Inputs
- Policy rules
- Input, tool args, output

## Outputs
- Structured verdict + reason
- Safe response

## Failure modes
- Verdict as prose, not structured.
- Over-blocking legitimate use.
- Injection bypasses a single layer.

## Minimal example
```python
def block(tool, args, ctx):
    if tool.name == "run_shell" and "rm -rf" in args.get("cmd", ""):
        return {"status": "blocked", "reason": "destructive"}
agent = LlmAgent(name="safe", tools=[run_shell], before_tool_callback=block)
```

## Next skills
- If blocked action needs a person: load `human-in-the-loop`
- If block rates must be measured: load `evaluation-monitoring`
