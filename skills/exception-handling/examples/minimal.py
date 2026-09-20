"""Exception Handling and Recovery — minimal runnable demo (stdlib only)."""
class TransientError(Exception): pass

def primary(q):
    if "flaky" in q: raise TransientError("timeout")
    return f"primary: {q}"

def fallback(q): return f"FALLBACK (degraded): {q}"

for q in ["hello", "flaky query"]:
    try: print(primary(q))
    except TransientError: print(fallback(q))
