"""Human approval gate: risky proposals stop for a redacted review before execution.

Real framework: Google ADK `escalate_to_human` tool on an Agent, with a
before_model_callback that redacts state before the reviewer sees it.
Run: python3 examples/minimal.py
"""

THRESHOLD = 0.6
AUDIT = []


def llm(prompt: str) -> dict:
    """Fake planner: returns a proposed action with a risk score."""
    risky = "delete" in prompt or "refund" in prompt
    return {
        "summary": f"execute: {prompt}",
        "effects": "drops 12k rows" if risky else "sends one email",
        "risk": 0.9 if risky else 0.1,
        "contact": "ada@example.com",
    }


def redact(proposal: dict) -> dict:
    return {**proposal, "contact": "[REDACTED]"}


def reviewer_ask(proposal: dict) -> str:
    """Canned human: approves anything that is not a deletion."""
    print(f"  REVIEW  {proposal['summary']} | effects={proposal['effects']} "
          f"| contact={proposal['contact']}")
    return "reject: needs a backup first" if "drops" in proposal["effects"] else "approve"


def handle(request: str) -> str:
    proposal = llm(request)
    decision = "auto-approve"
    if proposal["risk"] >= THRESHOLD:
        decision = reviewer_ask(redact(proposal))
        if not decision.startswith("approve"):
            AUDIT.append((proposal["summary"], decision))
            return f"ABORTED ({decision})"
    result = f"EXECUTED ({proposal['effects']})"
    AUDIT.append((proposal["summary"], decision))
    return result


for req in ["send the welcome note", "delete the stale accounts"]:
    print(f"{req!r} -> {handle(req)}")

print(f"audit records: {len(AUDIT)}")
for summary, decision in AUDIT:
    print(f"  {decision:<28} {summary}")
