---
name: guardrails
description: Use when inputs, tool args, or outputs need policy enforcement. Do not use as the only safety layer for high-risk actions.
role: [safety]
chapter: 18
token_cost_estimate: 183
chains_with: [human-in-the-loop, exception-handling]
---

# Guardrails and Safety

## When to use
- Untrusted user or tool input
- Tool args need validation pre-call
- Outputs need policy screening

## When NOT to use
- Fully trusted closed-loop system
- Only layer for high-risk acts (add human)
- Policy is undefined — define it first

## Inputs
- Policy (jailbreak, PII, scope rules)
- Pre-tool args or raw input

## Outputs
- ALLOW/BLOCK + reason
- Logged decision

## Failure modes
- Bypass — layer filters (input, tool, output), not one
- Over-block — measure false-positive rate, tune
- Silent blocks — always log reason + input hash

## Minimal example
```python
verdict = guardrail.check(input, policy)  # jailbreak/PII/scope
if verdict.block: log_and_refuse(verdict.reason)
validate_tool_params(tool, args)  # pre-call gate
```

## Next skills
- If blocked case needs judgment: load `human-in-the-loop`
- If violation needs recovery: load `exception-handling`
