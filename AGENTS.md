# Agentic Design Patterns — 21 skills, one per book chapter

## Start
Fresh agent: follow [STANDUP.md](STANDUP.md). Else read `manifest.json`, load only the `skills/<id>/SKILL.md` you need; `references/` for detail.

## Role -> Skills
- planner: routing, planning, multi-agent, goal-setting, a2a, resource-aware-optimization, prioritization, exploration-discovery
- executor: prompt-chaining, routing, parallelization, tool-use, multi-agent, mcp, a2a
- critic: reflection, learning-adaptation, reasoning-techniques, evaluation-monitoring, exploration-discovery
- memory: memory-management, learning-adaptation, mcp, rag
- safety: exception-handling, human-in-the-loop, guardrails

## Rules
- Do not load the entire PDF during normal execution. Use skills first; consult canonical PDF-derived slices (`ground-truth/`) when fidelity, ambiguity, provenance or missing detail requires it. PDF is for humans.
- Do not load all skills at once. Lazy-load only.
- Labels: SOURCE = book; DERIVED = ours (all SKILL.md/patterns.md code); EXTERNAL-UNVERIFIED/UNCERTAIN = unchecked.
- Never skip auth, confirmation or guardrails.
- New skill: update `manifest.json`, run `python3 tools/validate.py`. Runtimes: `models/`.
