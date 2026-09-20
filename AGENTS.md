# Agentic Design Patterns — Agent Guide

A skill library derived from "Agentic Design Patterns" (Gulli, 21 chapters).
Each chapter -> one self-contained skill in `skills/<id>/`.

## Navigate
1. Read `manifest.json` for the skill index (id, chapter, role, when to use, chains_with).
2. Pick the skills that match your role and the task.
3. Load `skills/<id>/SKILL.md` (<= 400 tokens each).
4. Load `skills/<id>/references/patterns.md` only when you need prompts or code detail.
5. `skills/<id>/examples/minimal.py` is a runnable, dependency-free sketch.

## Role -> Skills
- planner:  routing, planning, multi-agent, goal-setting, a2a, resource-aware-optimization, prioritization, exploration-discovery
- executor: prompt-chaining, routing, parallelization, tool-use, multi-agent, mcp, a2a
- critic:   reflection, learning-adaptation, reasoning-techniques, evaluation-monitoring, exploration-discovery
- memory:   memory-management, learning-adaptation, mcp, rag
- safety:   exception-handling, human-in-the-loop, guardrails

## Rules
- Do not read the PDF. It is for humans.
- Do not load all skills at once. Lazy-load: manifest -> 2-5 SKILL.md -> references on demand.
- Follow `chains_with` / "Next skills" in each SKILL.md to move between skills.
- Update `manifest.json` when adding a skill; keep SKILL.md body <= 400 tokens.
- See `models/` for per-model guidance (Fable 5.1, Grok 4.6, Muse).

## Layout
`manifest.json` index | `models/` profiles | `skills/<id>/{SKILL.md,references/patterns.md,examples/minimal.py}`
| `chapter_notebooks/Chapter_XX_*.SKILL.md` companions next to each notebook.
