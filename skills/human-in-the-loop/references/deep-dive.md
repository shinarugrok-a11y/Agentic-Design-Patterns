# Human-in-the-Loop (HITL) — deep dive

Source: Chapter 13 (GT:L7808–L8156) + `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`.
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

## Aspects (SOURCE, GT:L7856–L7872)
- **Human oversight**: monitoring agent performance and output.
- **Intervention and correction**: humans step in when the agent is stuck or wrong.
- **Human feedback for learning**: corrections and preferences shape the agent.
- **Decision augmentation**: agent supplies analysis, human decides.
- **Human-agent collaboration**: agent handles routine, human handles judgment.
- **Escalation policies**: explicit rules for when to hand off.

Human-on-the-loop (SOURCE, GT:L7945–L7955): experts set policy and the agent
acts within it, e.g. "70% tech stocks and 30% bonds, do not invest more than
5% in any single company, and automatically sell any stock that falls 10%
below its purchase price."

Drawbacks (SOURCE, GT:L7882–L7895, L8128–L8133): lack of scalability,
dependence on skilled operators, and the need to anonymize sensitive data
before a human sees it.

Rule of thumb (SOURCE, GT:L8099): domains where errors have significant
safety, ethical or financial consequences.

## Use cases named in the chapter (SOURCE, GT:L7902–L7938)
Content moderation, autonomous driving handover, financial fraud detection,
legal document review, complex customer support, data labeling, generative
AI refinement, autonomous networks.

## Book example: support agent with an escalation tool (ADK)
Provenance: SOURCE (abridged) — from GT:L7981–L8020 / notebook cell of `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`; imports trimmed, instruction verbatim.
```python
def troubleshoot_issue(issue: str) -> dict:
    return {"status": "success", "report": f"Troubleshooting steps for {issue}."}

def create_ticket(issue_type: str, details: str) -> dict:
    return {"status": "success", "ticket_id": "TICKET123"}

def escalate_to_human(issue_type: str) -> dict:
    # This would typically transfer to a human queue in a real system
    return {"status": "success", "message": f"Escalated {issue_type} to a human specialist."}

technical_support_agent = Agent(
    name="technical_support_specialist",
    model="gemini-2.0-flash-exp",
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
    tools=[troubleshoot_issue, create_ticket, escalate_to_human]
)
```

### WEAK: what this example does not do (verified against GT:L7981–L8070)
- The three tools are placeholders ("replace with actual implementations",
  GT:L7988). `escalate_to_human` returns `"status": "success"` immediately:
  no human is contacted and nothing waits for a decision.
- There is no approval step, no timeout rule and no deny default. Do not
  copy the stub's return value; a real escalation is *pending* until a human
  answers. See `examples/minimal.py` for a gate that holds by default,
  denies on timeout or silence, and executes only on explicit APPROVE.
- `personalization_callback` (GT:L8025–L8053) is defined but never attached
  to the agent in the book or the notebook (no `before_model_callback=`).
- It inserts content with `role="system"` into `llm_request.contents`;
  whether current ADK/Gemini accepts that role there is UNCERTAIN.

### Personalisation callback
Provenance: SOURCE (abridged) — condensed from GT:L8025–L8053.
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
DERIVED advice: put whatever the human will need (history, tier, steps
tried) into state *before* escalation so the hand-off carries it.

## Escalation policy template
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
Escalate to a human when ANY holds:
- action is irreversible (payment, deletion, external send): always, each time; no standing pre-approval
- confidence < {threshold} or the request is ambiguous after one clarification
- user expresses distress, legal threat, or requests a human
- policy/regulatory domain: {list}
Include in the handoff: summary, steps tried, tool results, user sentiment.
While waiting: status is pending_human; do not act.
```

## Confirmation gate (for personal/secure agents)
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
Proposed action: {action} on {target}. Effect: {effect}. Reversible: {yes/no}.
Reply APPROVE to proceed, or describe changes.
```
Never treat silence, a timeout or an unclear reply as approval: the action
stays held (`pending_human`) or is `denied`, and the case is logged.

## Feedback capture (DERIVED)
Store human decisions with the case id so they can be replayed as
evaluation data (`evaluation-monitoring`) or used to adapt policies
(`learning-adaptation`).

## Pattern variants (SOURCE terms; glosses DERIVED)
- **Escalation gate** — the agent calls an escalation tool when a case exceeds its competence. The book's version is a stub; a real one returns pending and waits.
- **Decision augmentation** — agent analyses and recommends, human makes the call.
- **Human-on-the-loop** — human sets policy up front, agent executes autonomously inside it (GT:L7945). In this repo it never covers irreversible actions; those keep a per-action APPROVE.
- **Intervention and correction** — human patches a stuck or wrong run mid-flight.
- **Feedback for learning** — approvals, edits and labels are logged as training signal.

## More prompt templates
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
You are a {domain} specialist. Resolve the request autonomously when you can.
Escalate with escalate_to_human(issue_type, details) when ANY holds:
- the action is irreversible or exceeds {threshold};
- policy is ambiguous or the case is borderline;
- the user is distressed, or you have already retried twice.
After escalating, wait: do not perform the action until a human approves.
```

Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
REVIEW REQUEST — {action_type}, risk {score}
Proposed action: {one_line_summary}
Effects if approved: {diff}
Agent rationale: {why}
Evidence: {citations}
Unknowns the agent could not resolve: {open_questions}
Reply exactly one of: APPROVE | REJECT <reason> | EDIT <revised action>
No reply = REJECT.
```

## Framework notes
- **Google ADK** (SOURCE) — escalation is an ordinary tool; `CallbackContext.state` carries customer data into a callback.
- **LangChain** (SOURCE, GT:L7978–L7979) — the chapter only says LangChain "also provides tools to implement these types of interactions". No LangChain code. A LangGraph interrupt-before-tool design is DERIVED, not in the chapter.

## Failure modes in depth (DERIVED)
- **Escalating everything** — gate on an explicit risk score plus reversibility, and track escalation rate.
- **Requests lacking context** — send summary, effects, rationale and open questions in one payload.
- **Rubber-stamping under volume** — the book names lack of scalability as the main drawback; pre-filter by policy, and sample-audit the low-risk items that policy lets through unreviewed. Never let volume turn a required approval into an automatic one.
- **Sensitive data exposed to reviewers** — the chapter requires anonymization (GT:L7894); redact before building the review payload.
- **Stub treated as a gate** — an escalation tool that returns success without a human is not HITL.
