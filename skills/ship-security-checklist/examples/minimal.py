"""Ship-security checklist: PASS / FAIL / BLOCKED per item; ship only if all PASS + reviewed.

Offline, DERIVED (operational; not a book chapter). Checks run on in-memory
files so the example needs no repository access.
"""
import re

SECRET = re.compile(r"(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.I)
EMAIL = re.compile(r"\b[\w.+-]+@(?!example\.(?:com|org)\b)[\w-]+\.[\w.]+\b")
RUBRIC = ("correct", "labelled", "complete", "clear", "safe")


def scan(files: dict, pattern: re.Pattern) -> tuple[str, str]:
    if not isinstance(files, dict) or not files:
        return "BLOCKED", "no files supplied"
    hits = [name for name, text in files.items() if not isinstance(text, str) or pattern.search(text)]
    return ("FAIL", f"matches in {hits}") if hits else ("PASS", f"{len(files)} files, 0 matches")


def review(scores: dict | None, reviewer: str | None) -> tuple[str, str]:
    if not scores or set(scores) != set(RUBRIC) or not all(isinstance(v, int) and 1 <= v <= 5 for v in scores.values()):
        return "BLOCKED", "rubric incomplete"
    if not reviewer:
        return "BLOCKED", "no human sign-off"
    low = [k for k, v in scores.items() if v < 3]
    return ("FAIL", f"low scores {low}") if low else ("PASS", f"scored by {reviewer}")


def checklist(files: dict, validator_exit: int | None, scores: dict | None, reviewer: str | None) -> dict:
    items = {"secrets": scan(files, SECRET), "personal data": scan(files, EMAIL)}
    items["validator"] = (("BLOCKED", "not run") if validator_exit is None
                          else ("PASS", "exit 0") if validator_exit == 0 else ("FAIL", f"exit {validator_exit}"))
    items["review rubric"] = review(scores, reviewer)
    ship = all(status == "PASS" for status, _ in items.values())
    return {"items": items, "ship": "YES" if ship else "NO"}


if __name__ == "__main__":
    good = {"a.py": "key = os.environ['LLM_API_KEY']", "README.md": "contact: someone@example.com"}
    scores = dict.fromkeys(RUBRIC, 4)
    cases = [
        ("all pass", good, 0, scores, "<reviewer role>", "YES"),
        ("hardcoded key", {**good, "b.py": "api_key = 'abcdefghijklmnop1234'"}, 0, scores, "<reviewer role>", "NO"),
        ("validator not run", good, None, scores, "<reviewer role>", "NO"),
        ("no sign-off", good, 0, scores, None, "NO"),
    ]
    for name, files, vexit, sc, who, want in cases:
        out = checklist(files, vexit, sc, who)
        print(f"{name:18} ship={out['ship']}  " + "; ".join(f"{k}={s}" for k, (s, _) in out["items"].items()))
        if out["ship"] != want:
            raise SystemExit(f"checklist wrong for {name!r}")
