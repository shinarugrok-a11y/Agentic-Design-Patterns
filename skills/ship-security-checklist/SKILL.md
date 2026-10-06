---
name: ship-security-checklist
description: One pre-ship gate. Every item PASS with evidence plus a review, or ship=NO. Operational, not a book chapter.
role: [safety]
chapter: null
kind: operational
token_cost_estimate: 240
chains_with: [guardrails, evaluation-monitoring, human-in-the-loop]
---

# Ship-Security Checklist (operational)

## When to use
- Before a PR, release, deploy or hand-over.
- Gate G1 in `templates/gates.md` points here.

## When NOT to use
- Private drafts nobody else runs.
- Instead of runtime `guardrails`.

## Inputs
- Change set
- Evidence per item

## Outputs
- PASS / FAIL / BLOCKED per item
- ship YES or NO

## Failure modes
- Ticked with no evidence: count as BLOCKED.
- Unknown treated as pass.
- A second near-duplicate checklist.

## Minimal example
```
items: secrets, personal data, least privilege, fail closed, no self-auth
       or auto-send, inputs validated, errors not leaked, tests green, review
status per item: PASS | FAIL | BLOCKED   (no evidence -> BLOCKED)
ship = YES only if all PASS and a human reviewer signed off
```

## Next skills
- If a runtime policy is missing: load `guardrails`
- If the review needs scoring: load `evaluation-monitoring`
- If sign-off is needed: load `human-in-the-loop`
