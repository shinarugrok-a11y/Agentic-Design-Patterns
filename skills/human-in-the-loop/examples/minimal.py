"""Human-in-the-Loop — minimal runnable demo (stdlib only)."""
def auto_fix(issue): return ("fixed", 0.9) if "password" in issue else (None, 0.3)

def escalate(issue): return f"TICKET opened for human: {issue}"

for issue in ["password reset", "refund dispute"]:
    fix, conf = auto_fix(issue)
    print(fix if conf >= 0.7 else escalate(issue))
