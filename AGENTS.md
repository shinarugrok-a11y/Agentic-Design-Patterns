# Agentic Design Patterns — agent entry point

Single entry file: 21 pattern skills (one per book chapter) plus 1 operational skill. Do the boot steps in order. If a Done check fails, stop and say which.

## Boot
1. **Runtime.** Write one line naming your runtime and model, or "unknown".
   Done: you can say that line.
2. **Profile.** Lowercase the line; the first row below with a substring signal wins, `*` is the fallback. Load only that file.
   Done: you can name the one `models/*.md` loaded.
3. **Gates.** Read [templates/gates.md](templates/gates.md), the one gate policy. Unknown = BLOCKED.
   Done: you can say which gate covers sending, paying or deleting.
4. **Index.** Read the generated [skills/INDEX.md](skills/INDEX.md). `manifest.json` is for tools; skip it.
   Done: you can state its pick rule.
5. **Pick.** Apply the pick rule. Load at most 3 `skills/<id>/SKILL.md`, or none.
   Done: you can list the ids loaded.
6. **Detail on demand.** `references/patterns.md`, then `references/deep-dive.md` (`Provenance:` lines mark book code). For book wording read one range from [ground-truth/INDEX.md](ground-truth/INDEX.md).
   Done: every "the book says" has a GT:L line.
7. **Self-check.**
   a. One profile; b. 3 or fewer skills;
   c. no gate broken: nothing irreversible without a per-action human APPROVE;
   d. never skip auth, confirmation or guardrails; secrets only from env vars;
   e. UNVERIFIED, UNCERTAIN and EXTERNAL-UNVERIFIED claims treated as unchecked.
   Done: all five are yes.

Stand-up budget: 4000 tokens (cl100k) for this file, the gates, one profile, the index and the picked cards. DERIVED.

| runtime signal | profile |
|---|---|
| muse | models/muse.md |
| fable 5.1, fable-5-1 | models/fable-5-1.md |
| grok 4.6, grok-4-6 | models/grok-4-6.md |
| codex, claude code, cursor, gemini cli, agy, coding agent, cli agent | models/coding-cli-agent.md |
| grok bot, desktop, chat assistant, personal assistant, browser agent | models/desktop-assistant-agent.md |
| * | models/desktop-assistant-agent.md |

## Role -> Skills
- planner: routing, planning, multi-agent, goal-setting, a2a, resource-aware-optimization, prioritization, exploration-discovery
- executor: prompt-chaining, routing, parallelization, tool-use, multi-agent, mcp, a2a
- critic: reflection, learning-adaptation, reasoning-techniques, evaluation-monitoring, exploration-discovery
- memory: memory-management, learning-adaptation, mcp, rag
- safety: exception-handling, human-in-the-loop, guardrails, ship-security-checklist

## Rules
- Do not load the entire PDF during normal execution. Use skills first; for fidelity or missing detail read one `ground-truth/` range. The PDF is for humans.
- Do not load all skills at once. Lazy-load only.
- Labels: SOURCE is the book; DERIVED is ours (all SKILL.md, patterns.md and `templates/`); the rest are unchecked.
- Maintainers: edit `manifest.json`, then `python3 tools/validate.py --sync`.
- Discovery: Codex and Claude Code read this file natively (Claude Code only with no `CLAUDE.md`); Gemini CLI via `GEMINI.md`. Cursor and Grok: UNVERIFIED.
