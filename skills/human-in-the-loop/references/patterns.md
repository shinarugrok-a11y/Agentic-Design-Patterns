# Human-in-the-Loop (HITL) — reference patterns

Source: Chapter 13 + `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`.

## Aspects (book)
- **Oversight**: humans monitor logs/dashboards for drift or misbehaviour.
- **Intervention & correction**: agent hands off when stuck or uncertain.
- **Feedback for learning**: human ratings/corrections become training or
  memory signal (RLHF-style).
- **Decision augmentation**: agent proposes, human decides.
- **Collaboration**: agent handles routine, human handles judgment.
- **Escalation policies**: explicit criteria for when to hand off.
- Variation "human-on-the-loop": humans set policy; agent acts within it in
  real time (e.g. trading rules: 70/30 allocation, <=5% per stock, auto-sell at -10%).

Drawbacks: does not scale (accuracy vs. volume trade-off), needs skilled
domain experts, operator training, privacy/anonymisation of data shown to
humans.

## Use cases named in the chapter
Content moderation (ambiguous cases escalated), autonomous driving handover,
fraud alerts to analysts, legal document review, complex/emotional customer
support, data labelling, generative content editing, autonomous network
operations (high-risk changes approved by analysts).

## Notebook pattern: support agent with escalation tool (ADK)
```python
def troubleshoot_issue(issue: str) -> dict:
    return {"status": "success", "report": f"Troubleshooting steps for {issue}."}

def create_ticket(issue_type: str, details: str) -> dict:
    return {"status": "success", "ticket_id": "TICKET123"}

def escalate_to_human(issue_type: str) -> dict:
    # transfers to a human queue in a real system
    return {"status": "success", "message": f"Escalated {issue_type} to a human specialist."}

technical_support_agent = Agent(name="technical_support_specialist", model="gemini-2.0-flash-exp",
    instruction="""
You are a technical support specialist for our electronics company.
FIRST, check if the user has a support history in state["customer_info"]["support_history"]. If they do, reference this history in your responses.
For technical issues:
1. Use the troubleshoot_issue tool to analyze the problem.
2. Guide the user through basic troubleshooting steps.
3. If the issue persists, use create_ticket to log the issue.
For complex issues beyond basic troubleshooting:
1. Use escalate_to_human to transfer to a human specialist.
Maintain a professional but empathetic tone. Acknowledge the frustration technical issues can cause, while providing clear steps toward resolution.
""",
    tools=[troubleshoot_issue, create_ticket, escalate_to_human])
```
Escalation is *a tool*, so the policy lives in the instruction and the
handoff is an auditable tool call.

### Personalisation via `before_model_callback`
```python
def personalization_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmRequest]:
    customer_info = callback_context.state.get("customer_info")
    if customer_info:
        note = (f"\nIMPORTANT PERSONALIZATION:\n"
                f"Customer Name: {customer_info.get('name', 'valued customer')}\n"
                f"Customer Tier: {customer_info.get('tier', 'standard')}\n")
        if customer_info.get("recent_purchases"):
            note += f"Recent Purchases: {', '.join(customer_info['recent_purchases'])}\n"
        if llm_request.contents:
            llm_request.contents.insert(0, types.Content(role="system", parts=[types.Part(text=note)]))
    return None      # None = continue with the modified request
```
Whatever context the human will need (history, tier, purchases) should be in
state *before* escalation so the handoff carries it.

## Escalation policy template
```
Escalate to a human when ANY holds:
- action is irreversible (payment, deletion, external send) and not pre-approved
- confidence < {threshold} or the request is ambiguous after one clarification
- user expresses distress, legal threat, or requests a human
- policy/regulatory domain: {list}
Include in the handoff: summary, steps tried, tool results, user sentiment.
```

## Confirmation gate (for personal/secure agents)
```
Proposed action: {action} on {target}. Effect: {effect}. Reversible: {yes/no}.
Reply APPROVE to proceed, or describe changes.
```
Never treat silence or a timeout as approval; default to no-op and log.

## Feedback capture
Store human decisions with the case id so they can be replayed as
evaluation data (`evaluation-monitoring`) or used to adapt policies
(`learning-adaptation`).
