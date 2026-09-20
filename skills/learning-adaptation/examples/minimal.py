"""Learning and Adaptation — minimal runnable demo (stdlib only)."""
import random

def fitness(p): return sum(p)  # higher is better
best = [random.random() for _ in range(5)]
for gen in range(20):
    cand = [x + random.uniform(-0.2, 0.2) for x in best]
    if fitness(cand) > fitness(best):
        best = cand
        print(f"gen {gen}: improved to {fitness(best):.3f}")
print("BEST:", [round(x, 2) for x in best])
