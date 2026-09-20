"""Guardrails and Safety — minimal runnable demo (stdlib only)."""
import re

BLOCKED = re.compile(r"(password|api[_-]?key|ssn)", re.I)

def guard(text):
    if BLOCKED.search(text):
        return (False, "blocked: sensitive data", ["pii"])
    return (True, "ok", [])

for t in ["Hello world", "my password is x"]:
    print(t, "->", guard(t))
