"""Evaluation and monitoring: accuracy, latency, tokens, trajectory, rubric judge.

Offline stub. `judge` mimics an LLM-as-a-Judge returning rubric JSON; the
other metrics are deterministic.
"""
import json
import time


def semantic_match(a: str, b: str) -> float:
    """Token-overlap proxy; exact match would score a paraphrase 0."""
    wa, wb = set(a.lower().replace(".", "").split()), set(b.lower().replace(".", "").split())
    return round(len(wa & wb) / len(wa | wb), 2)


def timed(fn, *args):
    t0 = time.perf_counter()
    out = fn(*args)
    return out, round((time.perf_counter() - t0) * 1000, 2)


def trajectory_score(actual: list[str], expected: list[str]) -> dict:
    in_order = actual == expected
    precision = len(set(actual) & set(expected)) / max(len(actual), 1)
    return {"in_order": in_order, "tool_precision": round(precision, 2)}


def judge(question: str) -> dict:
    """Stand-in for a rubric-driven LLM judge (temperature ~0.2, JSON output)."""
    leading = question.lower().startswith("don't you agree")
    vague = len(question.split()) < 8
    scores = {"clarity": 2 if vague else 5, "neutrality": 1 if leading else 5,
              "relevance": 4, "completeness": 2 if vague else 5, "audience": 4}
    overall = round(sum(scores.values()) / len(scores))
    action = "Revise for neutrality" if leading else "Clarify scope" if vague else "Approve as is"
    return {"overall_score": overall, "detailed_feedback": scores, "recommended_action": action}


class Monitor:
    def __init__(self):
        self.tokens_in = self.tokens_out = 0
        self.latencies: list[float] = []

    def record(self, prompt: str, response: str, latency_ms: float):
        self.tokens_in += len(prompt.split()) * 4          # replace with provider token counter
        self.tokens_out += len(response.split()) * 4
        self.latencies.append(latency_ms)

    def summary(self) -> dict:
        return {"tokens_in": self.tokens_in, "tokens_out": self.tokens_out,
                "p50_latency_ms": sorted(self.latencies)[len(self.latencies) // 2]}


if __name__ == "__main__":
    agent = lambda q: "The capital of France is Paris."
    answer, ms = timed(agent, "capital of France?")
    print("accuracy:", semantic_match(answer, "Paris is the capital of France."))
    print("trajectory:", trajectory_score(["search", "answer"], ["search", "answer"]))
    print("judge:", json.dumps(judge("Don't you agree that privacy laws hinder innovation?")))
    m = Monitor(); m.record("capital of France?", answer, ms)
    print("monitor:", m.summary())
