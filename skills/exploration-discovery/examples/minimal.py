"""Exploration and discovery: generate -> multi-persona review -> rank -> evolve.

Offline stub of the Co-Scientist / Agent Laboratory loop. Hypotheses are
strings; reviewers are scripted personas; ranking is a simple tournament.
"""
import random

random.seed(11)
PERSONAS = {
    "insight": "harsh but fair reviewer expecting experiments that lead to insight",
    "impact": "harsh, critical but fair reviewer looking for impact",
    "novelty": "open-minded reviewer looking for ideas not proposed before",
}


def generate(question: str, k: int) -> list[str]:
    seeds = ["reuse drug A", "target pathway B", "combine A with B", "model C explains data", "new assay D"]
    return [f"{question}: {s}" for s in random.sample(seeds, k)]


def review(hypothesis: str, persona: str) -> dict:
    """Stand-in for the structured REVIEW JSON (Overall 1-10, Decision Accept|Reject)."""
    base = 4 + hash((hypothesis, persona)) % 5
    bonus = 2 if persona == "novelty" and "new" in hypothesis else 0
    overall = min(10, base + bonus)
    return {"persona": persona, "Overall": overall, "Decision": "Accept" if overall >= 6 else "Reject"}


def rank(hypotheses: list[str]) -> list[tuple[float, str]]:
    scored = []
    for h in hypotheses:
        reviews = [review(h, p) for p in PERSONAS]
        accepts = sum(r["Decision"] == "Accept" for r in reviews)
        mean = sum(r["Overall"] for r in reviews) / len(reviews)
        scored.append((mean + accepts, h))            # require breadth of approval, not one fan
    return sorted(scored, reverse=True)


def evolve(top: list[str]) -> list[str]:
    """Stand-in for the Evolution agent: simplify / synthesise / recombine."""
    return [f"{h} (refined)" for h in top] + [f"{top[0]} + {top[-1].split(': ')[-1]}"]


if __name__ == "__main__":
    question = "How to slow liver fibrosis"
    pool, rounds = generate(question, 4), 3
    for r in range(rounds):
        ranked = rank(pool)
        print(f"round {r + 1}: " + " | ".join(f"{s:.1f} {h}" for s, h in ranked[:3]))
        pool = evolve([h for _, h in ranked[:2]])
    print("final:", rank(pool)[0][1])
