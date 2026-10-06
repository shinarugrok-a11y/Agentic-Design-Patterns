# Agentic Design Patterns — agent entry point

This is the single entry file: 21 pattern skills, one per book chapter. Do the boot steps in order; each ends with a done-check. If a check fails, stop and say which.

## Boot
1. **Runtime.** Write one line naming your runtime and model; "unknown" if unsure.
   Done: you can say that line.
2. **Profile.** Lowercase the line. The first row below with a signal that is a substring wins; `*` is the fallback. Load only that file.
   Done: you can name the one `models/*.md` you loaded.
3. **Index.** Read [skills/INDEX.md](skills/INDEX.md), which is generated. `manifest.json` is for tools; skip it.
   Done: you can state the index's pick rule.
4. **Pick.** Apply the pick rule to the task. Load at most 3 `skills/<id>/SKILL.md`, or none.
   Done: you can list the ids you loaded (3 or fewer).
5. **Detail on demand.** Open `references/patterns.md`, then `references/deep-dive.md`; its `Provenance:` lines mark book code. For book wording, read one range from [ground-truth/INDEX.md](ground-truth/INDEX.md).
   Done: every "the book says" you repeat has a GT:L line.
6. **Self-check.**
   a. Profile named.
   b. 3 or fewer skills loaded.
   c. No send, pay, delete, share, publish or other irreversible action without an explicit human APPROVE; silence or a timeout means denied.
   d. Never skip auth, confirmation or guardrails; secrets only from env vars.
   e. EXTERNAL-UNVERIFIED, UNCERTAIN and UNVERIFIED claims are treated as unchecked.
   Done: all five are yes.

Stand-up budget: 4000 tokens (cl100k) for this file, one profile, the index and the picked cards. DERIVED, not from the book.

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
- safety: exception-handling, human-in-the-loop, guardrails

## Rules
- Do not load the entire PDF during normal execution. Use skills first; for fidelity, ambiguity, provenance or missing detail, read one line range of `ground-truth/`. The PDF is for humans.
- Do not load all skills at once. Lazy-load only.
- Labels: SOURCE is the book; DERIVED is ours, including all SKILL.md and patterns.md code; the rest are unchecked.
- New skill: edit `manifest.json`, then run `python3 tools/validate.py --sync`.
- Discovery: Codex and Claude Code read this file natively; Claude Code only when there is no `CLAUDE.md`. Gemini CLI reads it via `GEMINI.md`. Cursor and Grok are UNVERIFIED.
