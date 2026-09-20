"""Chapter 21 — Multi-persona review scores for an exploration report."""
PERSONAS = [
    "harsh but fair reviewer; expect insightful experiments",
    "critical reviewer looking for field impact",
    "open-minded reviewer looking for novelty",
]

def review_bundle(get_score, plan: str, report: str) -> str:
    return "\n".join(get_score(plan, report, p) for p in PERSONAS)
