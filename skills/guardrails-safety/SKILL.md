---
name: guardrails-safety
description: Layered input/output/tool policy. Use on autonomous or user-facing agents. Do NOT treat the model as the only control.
role: [safety]
chapter: 18
token_cost_estimate: 273
chains_with: [human-in-the-loop, exception-handling]
---

# Guardrails / Safety

## When to use
- Agent can take actions or talk to untrusted users
- Need before-tool validation, output schema, or LLM policy enforcer
- Limit blast radius (user_id match, allowlists)

## When NOT to use
- Decision requires a human (load `human-in-the-loop`)
- Problem is a crashed tool, not policy (load `exception-handling`)
- Internal scratch work with no side effects

## Inputs
- Payload + session identity
- Policy prompt or Pydantic model
- `before_tool_callback` / task `guardrail`

## Outputs
- Execute, block (`status: error`), or compliant JSON
- Triggered policy ids

## Failure modes
- Unsure → "safe" lets bad input through
- Stale competitor/brand lists
- Wrong callback signature so checks never run

## Minimal example
```python
def validate_tool_params(tool, args, tool_context):
    if args.get("user_id_param") != tool_context.state.get("session_user_id"):
        return {"status": "error", "error_message": "blocked"}
    return None
```

## Next skills
- If a human must approve: load `human-in-the-loop`
- If the block is a retryable failure: load `exception-handling`
