"""Planning — minimal runnable demo (stdlib only)."""
goal = "launch landing page"
plan = [("draft copy", []), ("build page", ["draft copy"]), ("review", ["build page"])]
done = set()
for step, deps in plan:
    assert all(d in done for d in deps), f"blocked: {step}"
    print("EXEC:", step)
    done.add(step)
print("GOAL DONE:", goal)
