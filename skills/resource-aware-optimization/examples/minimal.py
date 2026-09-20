"""Classify complexity, spend the cheapest adequate model, and track spend in aggregate.

Real framework: Google ADK QueryRouterAgent(BaseAgent) dispatching between a
gemini-2.5-flash Agent and a gemini-2.5-pro Agent.
Run: python3 examples/minimal.py
"""

TIERS = {"simple": ("flash", 0.01), "complex": ("pro", 0.50)}
BUDGET = 0.60
spent = 0.0


def classify(query: str) -> str:
    """Fake router: long or multi-step questions get the expensive tier."""
    return "complex" if len(query.split()) >= 8 or "why" in query.lower() else "simple"


def llm(model: str, query: str) -> str:
    """Fake models: the cheap tier answers shorter."""
    return f"[{model}] {'detailed' if model == 'pro' else 'brief'} answer to {query!r}"


def handle(query: str) -> str:
    global spent
    tier = classify(query)
    model, cost = TIERS[tier]
    if spent + cost > BUDGET:                  # aggregate check, not per call
        model, cost = TIERS["simple"]
        answer = llm(model, query)
        spent += cost
        return f"{answer}\n  DEGRADED: budget low, answered on the cheap tier"
    answer = llm(model, query)
    spent += cost
    return f"{answer}\n  tier={tier} cost={cost:.2f} spent={spent:.2f}"


for q in ["capital of France?",
          "why does the retry backoff double after each failed attempt?",
          "explain in detail how the router picks between the two model tiers"]:
    print(f"Q: {q}\n{handle(q)}\n")

print(f"total spent {spent:.2f} of budget {BUDGET:.2f}")
