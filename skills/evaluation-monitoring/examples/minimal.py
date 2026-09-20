"""Evaluation and Monitoring — minimal runnable demo (stdlib only)."""
import time

def accuracy(out, exp):
    return len(set(out.split()) & set(exp.split())) / max(1, len(set(exp.split())))

def timed(fn, *a):
    t = time.time()
    return fn(*a), round(time.time() - t, 4)

out, dt = timed(lambda: "the cat sat")
print("acc:", round(accuracy(out, "the cat sat"), 2), "| latency:", dt)
