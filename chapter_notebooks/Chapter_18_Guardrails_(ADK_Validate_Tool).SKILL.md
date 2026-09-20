---
name: guardrails
description: Layered input validation, output filtering and tool restrictions. Screen inputs, tool arguments and outputs against policy before the primary agent acts or responds. Do not rely on a single layer or on the primary model to police itself.
role: [safety]
chapter: 18
token_cost_estimate: 370
chains_with: [human-in-the-loop, exception-handling, evaluation-monitoring]
---

# Guardrails / Safety Patterns

## When to use
- Customer-facing or content-generating agents.
- Jailbreak/prompt-injection exposure.
- Tool calls touch sensitive data or actions.
- Brand, legal or compliance constraints.

## When NOT to use
- Internal, read-only, low-risk automation.
- Guardrail LLM is the same model as the primary (shared weaknesses).
- Ambiguity should escalate to a human: use `human-in-the-loop`.

## Inputs
- Policy directives
- Input/tool args/output to screen
- Structured verdict schema

## Outputs
- `safe|unsafe` or `compliant|non-compliant` verdict + reasoning
- Blocked call error dict
- Audit log

## Failure modes
- Verdict returned as prose; parser fails open.
- Over-blocking legitimate requests (recall vs. precision).
- Guardrail only on input; harmful output passes.
- Policy list hard-coded; brands/competitors not updated.

## Minimal example
```python
def validate_tool_params(tool, args, tool_context) -> Optional[dict]:
    if args.get("user_id_param") != tool_context.state.get("session_user_id"):
        return {"status": "error", "error_message": "Tool call blocked"}
    return None
agent = Agent(before_tool_callback=validate_tool_params, tools=[...])
# LLM guardrail: SAFETY_PROMPT -> {"decision": "safe|unsafe", "reasoning": ...}
# validate with pydantic; on ambiguity default to safe/compliant
```

## Next skills
- If borderline cases need a human: load `human-in-the-loop`
- If blocked call needs a fallback: load `exception-handling`
- If guardrail quality must be measured: load `evaluation-monitoring`
