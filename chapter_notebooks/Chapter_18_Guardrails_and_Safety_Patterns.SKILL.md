---
name: guardrails-safety
description: Layered input, output, and tool constraints. Layer input validation, output filtering, behavioral constraints, and tool restrictions around every agent call. Skip heavyweight moderation only in closed, offline runs with no user-facing output.
role: [safety]
chapter: 18
token_cost_estimate: 370
chains_with: [human-in-the-loop, tool-use, evaluation-and-monitoring]
---

# Guardrails and Safety Patterns

## When to use
- Output reaches users or external systems
- Input is untrusted or adversarial
- The domain is regulated or brand-sensitive

## When NOT to use
- Closed offline run with no user impact
- Over-blocking would make the agent useless
- A single check is mistaken for full coverage

## Inputs
- untrusted input
- policy and allow/deny rules
- tool permission scopes

## Outputs
- allow, block, or rewrite verdict
- sanitized input or output
- violation log

## Failure modes
- Single-layer defense bypassed by jailbreak or injection
- Over-blocking legitimate requests and eroding usefulness
- Guardrail latency and cost added to every call
- Static rules that decay as attack patterns evolve

## Minimal example
```python
if not input_guard(user_text):            # injection, toxicity, PII
    return REFUSAL
draft = agent.run(user_text, allowed_tools=SCOPED_TOOLS)  # restrict capability
verdict = output_guard(draft)             # toxicity, policy, leakage
return draft if verdict.ok else redact(draft, verdict)
```

## Next skills
- If a block needs judgment: load `human-in-the-loop`
- If tools need scoping: load `tool-use`
- If policies drift over time: load `evaluation-and-monitoring`
