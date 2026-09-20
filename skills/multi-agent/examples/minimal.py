"""Multi-Agent Collaboration — minimal runnable demo (stdlib only)."""
def researcher(t): return f"research({t})"
def writer(r): return f"article<= {r}"
def critic(a): return "PASS" if len(a) > 20 else "FAIL"

r = researcher("batteries")
a = writer(r)
for _ in range(2):
    if critic(a) == "PASS": break
    a = writer(r + " +revision")
print("FINAL:", a, "|", critic(a))
