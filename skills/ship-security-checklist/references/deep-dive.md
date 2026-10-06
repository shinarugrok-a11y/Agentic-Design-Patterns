# Ship-Security Checklist — deep dive (operational)

Kind: operational. This skill is not one of the book's 21 chapters. Everything
here is DERIVED unless a line cites GT:L (a line in
`ground-truth/agentic_design_patterns.txt`, SOURCE).

## Why one checklist
Near-duplicate gate skills drift: one says "ask first", another says "the plan
authorises it". This repo keeps one gate policy (`templates/gates.md`) and one
pre-ship checklist (this skill). Other skills and `models/` point here instead of
restating rules.

## Book anchors (SOURCE)
- Least privilege: "An agent should be granted the absolute minimum set of
  permissions required to perform its task" (GT:L11804–L11805).
- Checkpoint and rollback, as in a transactional system (GT:L11774–L11780).
- LLM-as-a-Judge assesses output against predefined criteria (GT:L12066–L12069);
  the book's example is a five-criterion rubric (GT:L12286–L12292).

## Status rules (DERIVED)
- PASS: the check ran and its output is attached.
- FAIL: the check ran and found a problem.
- BLOCKED: the check could not run, its tool is missing, it timed out, or there is
  no evidence. BLOCKED stops a ship exactly as FAIL does.

## Worked example
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```text
item               status   evidence
secrets            PASS     scan of 14 changed files: 0 matches
personal data      PASS     scan: 0 emails/hostnames outside placeholders
fail closed        PASS     guard self-test: missing/empty/mismatch blocked
validator          BLOCKED  tiktoken not installed; command not run
review rubric      PASS     5/4/4/5/5, reviewer: <reviewer role>
ship               NO       validator BLOCKED
```

## Teacher review (folded in)
A structured quality review of a doc or pack before merge. Use the rubric in
`patterns.md`. A model can draft scores, as the book's LLM-as-a-Judge does; the
sign-off is a human's (gate G1). Reviewers score evidence, not tone.

## Variants
- CI job: run `examples/minimal.py`-style evaluation on every PR; it never merges.
- Release train: the same items, plus a rollback plan per checkpoint.

## Failure modes
- Self-certification: the author agent marks its own work PASS with no evidence.
- Silent pass: a crashed or skipped check reported as green.
- Checklist sprawl: a second "security review" skill appears; merge it here.
