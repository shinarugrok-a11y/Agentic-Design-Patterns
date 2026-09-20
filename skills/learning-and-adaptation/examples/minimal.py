"""Evolutionary self-improvement: mutate a strategy, keep it only if fitness improves.

Real framework: OpenEvolve `evolve.run(iterations=1000)` over an initial program plus a
separate evaluator file, with SICA's asynchronous overseer reviewing the change log.
Run: python3 examples/minimal.py
"""

BUDGET = 6
REQUIRED = ["policy", "amount", "confirm"]  # held-out fitness set; mutation cannot touch it
CLAUSES = ["be polite", "cite the policy", "use emoji",
           "state the amount", "be brief", "confirm with the user"]


def llm_mutate(parent: str, step: int) -> str:
    """Fake LLM: proposes one variant of the parent prompt."""
    return f"{parent}; {CLAUSES[step % len(CLAUSES)]}"


def evaluate(candidate: str) -> float:
    return sum(k in candidate for k in REQUIRED) / len(REQUIRED)


def overseer_review(log: list) -> None:
    """Stands in for SICA's overseer LLM: no self-modification is kept unsupervised."""
    if not log:
        print("overseer: nothing accepted, baseline retained")
    elif len(log) > BUDGET // 2:
        print(f"overseer: {len(log)} rewrites in {BUDGET} rounds - flagging possible overfit")
    else:
        print(f"overseer: approved {len(log)} change(s) {log}")


best = "Answer the billing question"
archive = [(best, evaluate(best))]
log = []

for step in range(BUDGET):
    variant = llm_mutate(best, step)
    gain = evaluate(variant) - evaluate(best)
    print(f"step {step}: {'keep   ' if gain > 0 else 'discard'} (+{gain:.2f}) {variant!r}")
    if gain > 0:
        best = variant
        archive.append((variant, evaluate(variant)))
        log.append((step, round(gain, 2)))

print(f"\nfitness {evaluate(best):.2f} after {len(archive)} archived versions")
print(f"best: {best}")
overseer_review(log)
