# Human-in-the-Loop — Pattern reference

Load this file only when implementing `human-in-the-loop`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when judgment, approval, or irreversible actions require a human; do not fully automate high-stakes steps.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Human-in-the-loop design pattern.

## Notebooks (extracted)

Human-in-the-Loop

### Notebooks
- `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`

### Patterns
- **Escalation tool:** `escalate_to_human` for complex cases beyond automated troubleshooting
- **State-aware agent:** reads `state["customer_info"]["support_history"]` for personalization
- **Callback injection:** `personalization_callback` on `CallbackContext` inserts system message into `LlmRequest`
- **Workflow:** troubleshoot → create_ticket → escalate when needed

### Prompt templates
Technical support agent:
```
You are a technical support specialist for our electronics company.
FIRST, check if the user has a support history in state["customer_info"]["support_history"]. If they do, reference this history in your responses.
For technical issues:
1. Use the troubleshoot_issue tool to analyze the problem.
2. Guide the user through basic troubleshooting steps.
3. If the issue persists, use create_ticket to log the issue.
For complex issues beyond basic troubleshooting:
1. Use escalate_to_human to transfer to a human specialist.
Maintain a professional but empathetic tone.
```

Personalization callback injects:
```
IMPORTANT PERSONALIZATION:
Customer Name: {customer_name}
Customer Tier: {customer_tier}
Recent Purchases: ...
```

### Minimal code
```python
def personalization_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    info = callback_context.state.get("customer_info", {})
    note = f"\nIMPORTANT PERSONALIZATION:\nCustomer Name: {info.get('name')}\n..."
    llm_request.contents.insert(0, types.Content(role="system", parts=[types.Part(text=note)]))
    return None
```

### Caveats
- Tools are placeholders — replace with real ticketing/queue integrations
- Callback must return `None` to proceed with modified request
- No runnable demo loop in notebook — definition only

---

## Failure modes (skill-level)
- No escalation path → agent improvises
- Every turn waits on a human (throughput collapse)
- Callback forgets to return None and drops the request

## Chains with
`guardrails-safety`, `exception-handling`
