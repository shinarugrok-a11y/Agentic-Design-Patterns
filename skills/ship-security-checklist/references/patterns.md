# Ship-Security Checklist — patterns (operational, DERIVED)

Not a book chapter. Anchors: least privilege (GT:L11804–L11809), rubric review via LLM-as-a-Judge (GT:L12066–L12069).

## Pattern
1. Run each item's check; record PASS, FAIL or BLOCKED with command + output.
2. Unknown, skipped or unrunnable is BLOCKED.
3. Score the rubric; a model may pre-score, a human signs off.
4. ship = YES only if all PASS and signed; else NO, listing blockers.

## Items
- No secrets; env-var placeholders that fail clearly when missing.
- No real emails, hostnames, ports or account names.
- Least privilege: read-only where writes are not needed.
- Guards fail closed on missing, empty or unknown input.
- No self-auth, self-grant or auto-send (gates G2, G5).
- Inputs validated; users see generic errors.
- Validator and tests green offline.

## Review rubric (teacher review)
Score 1–5 with evidence: correct, labelled, complete, clear, safe. Any score under 3 is FAIL.

More: `deep-dive.md`; policy in `templates/gates.md`.
