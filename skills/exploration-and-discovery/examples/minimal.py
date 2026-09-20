"""Bounded generate-review-rank-evolve loop ending in a sandboxed experiment.

Real framework: Agent Laboratory's ReviewersAgent.inference(plan, report) over
get_score personas, plus the co-scientist Generation/Reflection/Ranking/Evolution agents.
Run: python3 examples/minimal.py
"""

ROUNDS = 2                          # stopping rule: never search unbounded
PERSONAS = {"insight": 1.0, "impact": 0.8, "novelty": 1.2}
MECHANISMS = ["phage tail binding", "plasmid transfer", "capsid swapping",
              "host receptor mimicry", "toxin export", "biofilm drift",
              "prophage induction", "efflux hitchhiking"]


def llm(persona: str, hypothesis: str) -> float:
    """Canned reviewer: returns this persona's 1-4 rating of the hypothesis."""
    seed = sum(ord(c) for c in hypothesis) % 4 + 1
    return seed + (1 if persona == "novelty" and "refined" in hypothesis else 0)


def generator(question: str, n: int):
    return [f"{m} explains {question}" for m in MECHANISMS[:n]]


def reviewer(h: str):
    """Three personas score independently so one critic's bias cannot decide."""
    return h, round(sum(w * llm(p, h) for p, w in PERSONAS.items()), 2)


def evolve(h: str) -> str:
    return "refined " + h


def experiment(h: str, sandbox: bool) -> str:
    assert sandbox, "never test a hypothesis against a live system"
    return f"sandbox experiment on '{h}' -> supported"


pool = generator("cf-PICI host range", n=8)
for rnd in range(ROUNDS):
    reviewed = sorted((reviewer(h) for h in pool), key=lambda r: -r[1])
    top = [h for h, _ in reviewed[:3]]
    print(f"round {rnd}: reviewed {len(pool)}, kept top 3")
    for h, s in reviewed[:3]:
        print(f"    {s:>5}  {h}")
    pool = top + [evolve(h) for h in top]

print(experiment(top[0], sandbox=True))
