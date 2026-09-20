"""Exploration and Discovery — minimal runnable demo (stdlib only)."""
import random

def review(plan): return random.uniform(0, 1)  # reviewer score
best, best_s = None, 0.0
for i in range(5):
    plan, s = f"hypothesis-{i}", review(i)
    if s > best_s: best, best_s = plan, s
print(f"EXPLORED 5 | BEST: {best} (score {best_s:.2f})")
