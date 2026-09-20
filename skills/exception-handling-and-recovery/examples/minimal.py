"""Guarded call: retry transient faults, fall back on permanent ones, escalate if neither works.

Real framework: Google ADK SequentialAgent(sub_agents=[primary_handler, fallback_handler,
response_agent]) branching on state["primary_location_failed"].
Run: python3 examples/minimal.py
"""

MAX_ATTEMPTS = 3
LOG = []


class Transient(Exception):
    """Timeout or 503 - safe to retry."""


class Permanent(Exception):
    """Invalid input or insufficient funds - retrying can never help."""


def precise_lookup(address: str, script: list) -> str:
    """Fake tool: raises whatever this scenario scripted for the current attempt."""
    fault = script.pop(0)
    if fault:
        raise fault
    return f"12.34,56.78 (precise) for {address}"


def general_area(address: str) -> str:
    return f"city-level area for {address}"  # degraded, but still useful


def guarded(address: str, script: list):
    for attempt in range(MAX_ATTEMPTS):
        try:
            return precise_lookup(address, script)
        except Transient as e:
            LOG.append(f"attempt {attempt}: transient {e}, backing off {2 ** attempt}s")
        except Permanent as e:
            LOG.append(f"attempt {attempt}: permanent {e}, no retry - using fallback")
            return general_area(address)
    LOG.append(f"no result after {MAX_ATTEMPTS} attempts")
    return None


for name, script in [("flaky st", [Transient("503"), None]),
                     ("!!bad!!", [Permanent("unparseable address")]),
                     ("down st", [Transient("503")] * MAX_ATTEMPTS)]:
    LOG.clear()
    result = guarded(name, list(script))
    for line in LOG:
        print(f"  {line}")
    print(f"{name}: {result or 'escalated to a human operator'}\n")
