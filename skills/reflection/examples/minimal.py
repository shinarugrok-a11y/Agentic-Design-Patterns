"""Reflection — minimal runnable demo (stdlib only)."""
def draft(b): return f"Ad: {b}!!!"
def critique(d): return "PASS" if "eco" in d.lower() else "FAIL: missing eco angle"

brief = "eco sneakers"
d = draft(brief)
for _ in range(3):
    notes = critique(d)
    print(d, "->", notes)
    if notes == "PASS": break
    d = draft(brief + " (eco angle)")
