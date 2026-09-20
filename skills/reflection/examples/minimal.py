"""Chapter 4 — Generate / critique / refine until CODE_IS_PERFECT or max_n."""

def reflect(generate, critique, refine, task: str, max_n: int = 3) -> str:
    draft = generate(task)
    for _ in range(max_n):
        review = critique(task, draft)
        if "CODE_IS_PERFECT" in review:
            return draft
        draft = refine(task, draft, review)
    return draft
