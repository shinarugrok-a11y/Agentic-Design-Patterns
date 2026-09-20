"""Reasoning Techniques — minimal runnable demo (stdlib only)."""
def cot_solve(problem):
    steps = [f"step{i}: partial of ({problem})" for i in range(1, 4)]
    answer = f"solved({problem})"  # would verify with code
    return steps, answer

steps, ans = cot_solve("23*17")
print("\n".join(steps))
print("ANSWER:", ans, "| check:", 23 * 17)
