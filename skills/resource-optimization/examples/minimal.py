"""Resource-Aware Optimization — minimal runnable demo (stdlib only)."""
COST = {"cheap": 1, "pro": 10}

def classify(p): return "pro" if any(k in p.lower() for k in ("prove", "derive", "analyze")) else "cheap"

def handle(p):
    tier = classify(p)
    return f"[{tier} cost={COST[tier]}] answer: {p[:40]}"

for p in ["What time is it?", "Analyze this contract risk"]: print(handle(p))
