"""Chapter 11 — Iterate until a True/False goals-met judge fires."""

def run_until_goals(generate, review, goals_met, use_case, goals, max_n=5):
    previous, feedback = "", ""
    for _ in range(max_n):
        code = generate(use_case, goals, previous, feedback)
        feedback = review(code, goals)
        if goals_met(feedback, goals):
            return code
        previous = code
    return previous  # best-effort; caller should flag incomplete
