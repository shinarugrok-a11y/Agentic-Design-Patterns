"""Human-in-the-loop: escalation policy + confirmation gate for risky actions.

Offline stub (DERIVED). The book's `escalate_to_human` (Ch 13, GT:L7997-L7999)
is a placeholder that returns "success" with no human involved; this stub
does not copy that. Rules enforced here:

- An escalated action never runs until a human explicitly replies APPROVE.
- With no approval channel attached (the default), the result is
  `pending_human`: the action is held, not executed and not approved.
- A channel that times out, returns nothing, or returns anything other than
  APPROVE yields `denied`.

`approver` is injectable: a callable taking the hand-off dict and returning
the human's reply (str), returning None, or raising TimeoutError. Replace it
with a real channel (UI, ticket queue, chat).
"""
from dataclasses import dataclass, field
from typing import Callable, Optional

ALWAYS_CONFIRM = {"send_email", "send_message", "pay", "refund", "delete_account",
                  "share", "publish", "schedule_for_others"}

Approver = Callable[[dict], Optional[str]]


@dataclass
class Action:
    name: str
    target: str
    irreversible: bool
    confidence: float

    def __post_init__(self):
        if not self.name or not self.target:
            raise ValueError("action name and target are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")


@dataclass
class Outcome:
    status: str                      # executed | pending_human | denied
    detail: str
    audit: list = field(default_factory=list)


def should_escalate(action: Action, threshold: float = 0.8) -> Optional[str]:
    if action.name in ALWAYS_CONFIRM:
        return f"{action.name} acts on someone's behalf and requires confirmation"
    if action.irreversible:
        return "irreversible action requires confirmation"
    if action.confidence < threshold:
        return f"low confidence ({action.confidence:.2f} < {threshold})"
    return None


def execute(action: Action) -> str:
    return f"executed {action.name} on {action.target}"


def run(action: Action, context: dict, approver: Optional[Approver] = None) -> Outcome:
    reason = should_escalate(action)
    if reason is None:
        return Outcome("executed", execute(action), ["auto: low risk, in policy"])
    handoff = {"reason": reason, "action": action.name, "target": action.target,
               "context": context, "reply_with": "APPROVE to proceed; anything else denies"}
    audit = [f"escalated: {reason}"]
    if approver is None:
        audit.append("no approval channel attached; action held")
        return Outcome("pending_human", f"awaiting human decision on {action.name}", audit)
    try:
        reply = approver(handoff)
    except TimeoutError:
        reply = None
    if reply is None or reply.strip().upper() != "APPROVE":
        audit.append(f"denied (reply={reply!r}); no answer means no")
        return Outcome("denied", f"not executed: {action.name}", audit)
    audit.append("approver replied APPROVE")
    return Outcome("executed", execute(action) + " (approver replied APPROVE)", audit)


def timed_out(_handoff: dict) -> Optional[str]:
    raise TimeoutError


if __name__ == "__main__":
    ctx = {"customer": "Jane", "tier": "gold", "steps_tried": ["restart", "reinstall"]}
    cases = [
        (Action("read_calendar", "jane", irreversible=False, confidence=0.95), None),
        (Action("send_email", "jane@example.com", irreversible=True, confidence=0.99), None),
        (Action("refund", "order-42", irreversible=True, confidence=0.99), timed_out),
        (Action("refund", "order-42", irreversible=True, confidence=0.99), lambda h: None),
        (Action("delete_account", "jane", irreversible=True, confidence=0.99), lambda h: "maybe"),
        (Action("refund", "order-42", irreversible=True, confidence=0.99), lambda h: "APPROVE"),
    ]
    results = []
    for action, approver in cases:
        out = run(action, ctx, approver)
        results.append(out.status)
        print(f"{action.name:15} -> {out.status:14} {out.detail}")
    # The APPROVE case uses a scripted approver; a real deployment needs a human on the channel.
    if results != ["executed", "pending_human", "denied", "denied", "denied", "executed"]:
        raise SystemExit(f"HITL gate wrong: {results}")
