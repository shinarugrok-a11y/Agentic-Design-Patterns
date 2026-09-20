"""Learning and adaptation: evolutionary improve-evaluate-archive loop.

Offline stub of the OpenEvolve / SICA shape: keep an archive of scored
versions, mutate the best, evaluate, and only promote on a held-out check.
"""
import random

random.seed(7)
TARGET = 0.75  # the "unknown" optimum the evaluator rewards


def evaluate(candidate: float) -> float:
    """Automatic, deterministic evaluator. Higher is better."""
    return 1.0 - abs(TARGET - candidate)


def holdout(candidate: float) -> float:
    """Independent check so we do not promote noise-fitted versions."""
    return 1.0 - abs(TARGET - candidate) ** 0.5


def mutate(parent: float) -> float:
    """Stand-in for: llm('Improve this program for <objective>...')"""
    return min(1.0, max(0.0, parent + random.uniform(-0.15, 0.15)))


def evolve(seed: float, iterations: int = 50) -> tuple[float, float]:
    archive = [(evaluate(seed), seed)]
    best_score, best = archive[0]
    for _ in range(iterations):
        parent = max(archive)[1]
        child = mutate(parent)
        archive.append((evaluate(child), child))
        if evaluate(child) > best_score and holdout(child) >= holdout(best):
            best_score, best = evaluate(child), child
    return best, best_score


if __name__ == "__main__":
    best, score = evolve(seed=0.1)
    print(f"best candidate={best:.3f} score={score:.3f}")
