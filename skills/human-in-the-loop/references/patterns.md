# Human-in-the-Loop — Patterns

## Pattern variants
- **Escalation gate** — agent calls an `escalate_to_human` tool when the case exceeds its competence; the default and cheapest variant.
- **Decision augmentation** — agent analyses and recommends, human makes the call; use where accountability is legally required (loan approval, sentencing, diagnosis).
- **Human-on-the-loop** — human sets policy up front, agent executes autonomously inside it; use when volume makes per-case review impossible (trading limits, call routing rules).
- **Intervention and correction** — human patches a stuck or wrong run mid-flight and supplies the missing data.
- **Feedback for learning** — approvals, edits, and labels are logged as training signal (RLHF, annotation); pairs with any variant above.

## Prompt templates

```
You are a {domain} specialist. Resolve the request autonomously when you can.
Escalate with escalate_to_human(issue_type, details) when ANY holds:
- the action is irreversible or exceeds {threshold};
- policy is ambiguous or the case is borderline;
- the user is distressed, or you have already retried twice.
Never guess on an escalation-triggering case. State why you escalated.
```

```
REVIEW REQUEST — {action_type}, risk {score}
Proposed action: {one_line_summary}
Effects if approved: {diff}
Agent rationale: {why}
Evidence: {citations}
Unknowns the agent could not resolve: {open_questions}
Reply exactly one of: APPROVE | REJECT <reason> | EDIT <revised action>
```

## Code patterns

Google ADK (escalation tool wired into the agent):
```python
def escalate_to_human(issue_type: str) -> dict:
    # transfers to a human queue in a real system
    return {"status": "success", "message": f"Escalated {issue_type} to a specialist."}

technical_support_agent = Agent(
    name="technical_support_specialist", model="gemini-2.0-flash-exp",
    instruction="""Troubleshoot first with troubleshoot_issue, log with create_ticket.
For complex issues beyond basic troubleshooting: use escalate_to_human.""",
    tools=[troubleshoot_issue, create_ticket, escalate_to_human],
)
```

Google ADK (`before_model_callback` injecting reviewer/customer context from state):
```python
def personalization_callback(callback_context: CallbackContext,
                             llm_request: LlmRequest) -> Optional[LlmRequest]:
    info = callback_context.state.get("customer_info")   # tier, history, purchases
    if info:
        note = f"Customer Name: {info['name']}\nCustomer Tier: {info['tier']}\n"
        llm_request.contents.insert(
            0, types.Content(role="system", parts=[types.Part(text=note)]))
    return None   # None = continue with the modified request
```

## Framework notes
- **LangChain / LangGraph** — the chapter notes LangChain offers equivalent interaction tools; in LangGraph this is an interrupt before the tool node, resumed with the reviewer's decision.
- **Google ADK** — escalation is an ordinary tool; `ToolContext` / `CallbackContext.state` carry the case file, and callbacks are the hook for redaction and context injection.

## Failure modes in depth
- **Escalating everything** — thresholds set on fear rather than measured risk; gate on an explicit risk score plus reversibility, and track escalation rate as an SLO.
- **Requests lacking context** — the reviewer sees a verdict, not the case; send summary, concrete effects, rationale, and open questions in one payload (template above).
- **Rubber-stamping under volume** — HITL does not scale to millions of cases; pre-filter automatically, sample-audit the auto-approved tail, and staff for the residual.
- **Sensitive data exposed to reviewers** — the chapter flags anonymization as a hard requirement; redact PII in the callback that builds the review payload, not in the reviewer UI.

## Source
Chapter 13 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb.
