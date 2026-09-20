# Agentic Design Patterns — Agent Guide

A skill library derived from "Agentic Design Patterns" (21 chapters).
Each chapter -> one self-contained skill in `skills/`.

## Navigate
1. Read `manifest.json` for the skill index.
2. Pick the skills that match your role.
3. Load `skills/<id>/SKILL.md`. Load `references/` only if you need detail.

## Role -> Skills
- planner:  routing, planning, multi-agent, goal-setting, a2a, resource-aware-optimization, prioritization, exploration-discovery
- executor: prompt-chaining, routing, parallelization, tool-use, multi-agent, mcp, a2a
- critic:   reflection, learning-adaptation, reasoning-techniques, evaluation-monitoring, exploration-discovery
- memory:   memory-management, learning-adaptation, mcp, rag
- safety:   exception-handling, human-in-the-loop, guardrails

## Rules
- Do not read the PDF. It is for humans.
- Do not load all skills at once. Lazy-load only.
- Update `manifest.json` when adding a skill (check: `python3 tools/validate.py`).
- See `models/` for per-model guidance (Fable 5.1, Grok 4.6, Muse).
