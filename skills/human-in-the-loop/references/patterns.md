# Human-in-the-Loop

Ch 13.

## Frameworks
- Google ADK (ToolContext, CallbackContext, LlmRequest personalization).

## Key APIs from the notebooks
- `troubleshoot_issue(issue) -> dict auto-resolution attempt`
- `create_ticket(issue_type, details) -> dict audit trail`
- `escalate_to_human(issue_type) -> dict handoff`

## Code patterns
- Pattern: auto-attempt -> confidence/policy check -> escalate with full context -> resume on decision.
- Always attach issue + attempted steps + confidence to the escalation.
- Set a timeout/default action while awaiting the human.

## Prompt templates
- Escalation message: `Issue: {issue}. Tried: {steps}. Confidence: {c}. Decision needed: {ask}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`

