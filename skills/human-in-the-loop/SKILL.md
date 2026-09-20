---
name: human-in-the-loop
description: Human approval gate on risky actions. Pause for human approval before any irreversible, high-risk, or ambiguous action. Skip it for reversible low-stakes actions where approval latency dominates the work.
role: [safety]
chapter: 13
token_cost_estimate: 360
chains_with: [guardrails-safety, exception-handling-and-recovery, evaluation-and-monitoring]
---

# Human-in-the-Loop

## When to use
- Action is irreversible or high-cost
- Input is ambiguous or policy-sensitive
- The domain requires accountable sign-off

## When NOT to use
- Action is cheap and reversible
- Approval latency outweighs the risk
- Volume would force reviewers to rubber-stamp

## Inputs
- proposed action and rationale
- escalation policy and thresholds
- reviewer channel

## Outputs
- approve, reject, or edit decision
- human feedback for later learning
- audit record

## Failure modes
- Escalating everything, which destroys throughput
- Approval requests lacking the context to decide
- Reviewer rubber-stamping under volume pressure
- Sensitive data exposed to reviewers without redaction

## Minimal example
```python
proposal = agent.plan_action(request)
if risk(proposal) >= THRESHOLD:
    decision = reviewer.ask(summary=proposal.summary,   # enough context to judge
                            diff=proposal.effects, redact=PII)
    if decision != "approve":
        return abort(decision)
execute(proposal); audit.record(proposal, decision)
```

## Next skills
- If you need automated pre-filters: load `guardrails-safety`
- If escalation follows a failure: load `exception-handling-and-recovery`
- If human feedback should be scored: load `evaluation-and-monitoring`
