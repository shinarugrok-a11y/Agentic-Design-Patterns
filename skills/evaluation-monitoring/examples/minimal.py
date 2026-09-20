"""Chapter 19 — Exact-match accuracy + latency wrapper (baseline monitors)."""
import time

def evaluate_response_accuracy(agent_output: str, expected_output: str) -> float:
    return 1.0 if agent_output.strip().lower() == expected_output.strip().lower() else 0.0

def timed_agent_action(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, (time.perf_counter() - start) * 1000
