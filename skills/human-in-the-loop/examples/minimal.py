"""Human-in-the-loop: escalation policy + confirmation gate for risky actions.

Offline stub. `ask_human` is replaced by a real channel (UI, ticket queue,
chat). Silence or timeout is never treated as approval.
"""
from dataclasses import dataclass


@dataclass
class Action:
    name: str
    target: str
    irreversible: bool
    confidence: float


def should_escalate(action: Action, threshold: float = 0.8) -> str | None:
    if action.irreversible:
        return "irreversible action requires confirmation"
    if action.confidence < threshold:
        return f"low confidence ({action.confidence:.2f} < {threshold})"
    return None


def ask_human(prompt: str, scripted_reply: str | None) -> str:
    """Stand-in for a real human channel; None simulates a timeout."""
    print("HUMAN? " + prompt)
    return scripted_reply or "TIMEOUT"


def execute(action: Action) -> str:
    return f"executed {action.name} on {action.target}"


def run(action: Action, context: dict, scripted_reply: str | None = None) -> str:
    reason = should_escalate(action)
    if reason is None:
        return execute(action)
    handoff = (f"{reason}. Proposed: {action.name} on {action.target}. "
               f"Context: {context}. Reply APPROVE to proceed.")
    reply = ask_human(handoff, scripted_reply)
    if reply.strip().upper() == "APPROVE":
        return execute(action) + " (human approved)"
    return f"no-op: awaiting human decision (reply={reply!r}); case logged"


if __name__ == "__main__":
    ctx = {"customer": "Jane", "tier": "gold", "steps_tried": ["restart", "reinstall"]}
    print(run(Action("send_email", "jane@example.com", irreversible=False, confidence=0.95), ctx))
    print(run(Action("refund", "order-42", irreversible=True, confidence=0.99), ctx, scripted_reply="APPROVE"))
    print(run(Action("delete_account", "jane", irreversible=True, confidence=0.99), ctx))
