"""Resource-aware optimisation: classify complexity, route to cheapest tier.

Offline stub. `classify` and `call_model` stand in for LLM calls; the cost
ledger and budget-triggered degradation are the pattern.
"""
TIERS = {"simple": "small-model", "reasoning": "reasoning-model", "internet_search": "large-model"}
COST_PER_1K = {"small-model": 0.15, "reasoning-model": 1.10, "large-model": 2.50}
DOWNGRADE = {"large-model": "reasoning-model", "reasoning-model": "small-model", "small-model": "small-model"}


def classify(prompt: str) -> str:
    """Stand-in for a JSON classifier prompt. Cheap heuristics are fine here."""
    p = prompt.lower()
    if any(w in p for w in ("today", "latest", "2026", "news")):
        return "internet_search"
    if any(w in p for w in ("why", "prove", "step", "how many")) or len(p.split()) > 20:
        return "reasoning"
    return "simple"


def call_model(model: str, prompt: str) -> tuple[str, int]:
    tokens = len(prompt.split()) * 4
    return f"[{model}] answer to: {prompt}", tokens


class Router:
    def __init__(self, budget_usd: float):
        self.budget, self.spend = budget_usd, 0.0

    def handle(self, prompt: str) -> dict:
        cls = classify(prompt)
        model = TIERS[cls]
        if self.spend > 0.9 * self.budget:            # graceful degradation
            model = DOWNGRADE[model]
        answer, tokens = call_model(model, prompt)
        cost = tokens / 1000 * COST_PER_1K[model]
        self.spend += cost
        return {"classification": cls, "model": model, "cost": round(cost, 5), "answer": answer}


if __name__ == "__main__":
    r = Router(budget_usd=0.05)
    for q in ["What is the capital of Australia?",
              "Explain step by step why quantum computers threaten RSA.",
              "What is the latest AI news today?",
              "What is the latest AI news today?"]:
        print(r.handle(q), f"total={r.spend:.4f}")
