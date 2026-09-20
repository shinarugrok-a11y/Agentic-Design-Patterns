"""Chapter 16 — Classify then pick a cheaper or stronger model."""

def handle_prompt(prompt: str, classify, generate, search=None) -> dict:
    classification = classify(prompt)["classification"]  # simple|reasoning|internet_search
    extra = search(prompt) if classification == "internet_search" and search else None
    answer, model = generate(prompt, classification, extra)
    return {"classification": classification, "response": answer, "model": model}
