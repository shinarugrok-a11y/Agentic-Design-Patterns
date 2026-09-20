# Agentic Design Patterns — Agent Guide

A skill library derived from "Agentic Design Patterns" (Gulli): 21 chapters, one
self-contained skill per chapter in `skills/`.

## Navigate
1. Read `manifest.json` for the skill index. The full file is ~5.1k tokens; when context is
   tight, slice it by role instead of reading it whole:
   `jq '[.skills[] | select(.role[] == "executor") | {id, when_to_use, chains_with}]' manifest.json`
2. Pick the skills matching your role and the task in front of you.
3. Load `skills/<id>/SKILL.md` (~375 tokens each). Load `skills/<id>/references/patterns.md`
   only when you need framework detail, prompt templates, or failure-mode mitigations.
4. Follow the "Next skills" section of a SKILL.md to decide what to load after it.

## Role -> Skills
- planner: `routing`, `planning`, `multi-agent-collaboration`, `goal-setting-and-monitoring`,
  `inter-agent-communication-a2a`, `resource-aware-optimization`, `prioritization`,
  `exploration-and-discovery`
- executor: `prompt-chaining`, `routing`, `parallelization`, `tool-use`,
  `multi-agent-collaboration`, `model-context-protocol`, `inter-agent-communication-a2a`
- critic: `reflection`, `learning-and-adaptation`, `reasoning-techniques`,
  `evaluation-and-monitoring`, `exploration-and-discovery`
- memory: `memory-management`, `learning-and-adaptation`, `model-context-protocol`,
  `knowledge-retrieval-rag`
- safety: `exception-handling-and-recovery`, `human-in-the-loop`, `guardrails-safety`

## Layout
- `manifest.json` — machine-readable index of all 21 skills.
- `skills/<id>/SKILL.md` — the card: when to use, inputs, outputs, failure modes, next skills.
- `skills/<id>/references/patterns.md` — on-demand detail, ~600-1000 tokens.
- `skills/<id>/examples/minimal.py` — runnable, dependency-free demo of the control flow.
- `models/` — per-model guidance for Fable 5.1, Grok 4.6, and Muse.
- `chapter_notebooks/Chapter_NN_*.SKILL.md` — the same card, reachable from the notebook path.

## Rules
- Do not read the PDF. It is 458 pages and it is for humans.
- Do not load all skills at once. Two or three SKILL.md files is a normal working set.
- Do not load `references/` by default; load it only when the SKILL.md is not enough.
- Keep every SKILL.md at or under 400 tokens. Detail belongs in `references/patterns.md`.
- Read `models/<your-model>.md` before deciding how many skills to load.
- When adding a skill: add its record to `manifest.json`, create
  `skills/<id>/{SKILL.md,references/patterns.md,examples/minimal.py}`, add the
  `chapter_notebooks/` companion, then run `python3 tools/validate_skills.py --sync`.
