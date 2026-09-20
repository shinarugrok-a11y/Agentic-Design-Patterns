---
name: exploration-discovery
description: Seek novel information and unknown unknowns. Use for research/ideation. Do NOT use for known-answer Q&A.
role: [planner, critic]
chapter: 21
token_cost_estimate: 248
chains_with: [reasoning-techniques, rag]
---

# Exploration and Discovery

## When to use
- Goal is novel ideas, literature, or experiments (unknown unknowns)
- Multi-role lab: postdoc / professor / reviewers
- Independent reviewer personas then Accept/Reject

## When NOT to use
- User wants a known fact (load `rag` or `tool-use`)
- Structured reasoning on a closed problem (load `reasoning-techniques`)
- Production FAQ

## Inputs
- Open-ended topic
- Phase list + context(phase)
- Review JSON schema (scores + Decision)

## Outputs
- Research plan and report
- Multi-reviewer JSON
- README / artifact bundle

## Failure modes
- Endless ideation, no decision
- One critic dominates
- Missing `query_model` / Agent Laboratory deps

## Minimal example
```python
reviews = [get_score(plan, report, persona) for persona in PERSONAS]
# JSON fields: Originality, Quality, Clarity, Significance, Overall, Decision
```

## Next skills
- If you need CoT/ToT/ReAct inside a phase: load `reasoning-techniques`
- If discovery is corpus retrieval: load `rag`
