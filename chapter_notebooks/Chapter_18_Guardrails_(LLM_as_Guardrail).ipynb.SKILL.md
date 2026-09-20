---
name: guardrails-safety
description: Validate inputs, tool params, and outputs against policy.
role: [safety]
chapter: 18
token_cost_estimate: 219
chains_with: [human-in-the-loop, evaluation-monitoring]
---

# Guardrails and Safety

## When to use
- Agent faces untrusted users or high-stakes actions.
- Validate at three gates: input, tool params, output.
- Policy checks use schemas or LLM judges.

## When NOT to use
- Fully trusted internal batch job.
- Guardrail latency breaks the use case.

## Inputs
- Policy rules + validation schemas
- Points to gate: input/tool/output

## Outputs
- Allow/block/flag decision + logged reason

## Failure modes
- Over-blocking kills legitimate use; tune precision.
- LLM judge guardrail is itself prompt-injectable.
- Gaps between gates let unsafe content through.

## Minimal example
```python
validate_tool_params(tool, params)  # schema gate
verdict = llm_judge(PolicyEvaluation, user_input)
allow, msg, flags = run_guardrail_crew(user_input)
```

## Next skills
- If blocked cases need human review: load `human-in-the-loop`
- If block rates need tracking: load `evaluation-monitoring`
