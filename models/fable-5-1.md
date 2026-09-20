# Fable 5.1

## Profile
- Context window: ~1M tokens
- Cost: high
- Use for: planning, long-horizon, multi-hour agentic work
- Preferred skill count: 10–15 `SKILL.md` files (never all 21)
- Owns roles: **planner** and **critic**

## Load order
1. `AGENTS.md`
2. `manifest.json` (index only)
3. Role-matched `skills/<id>/SKILL.md`
4. One `references/patterns.md` when implementing

## Should
- Own planning and critique; optionally one executor skill for a prototype.
- Pair `planning` / `goal-setting` with a stop condition.
- Keep `guardrails-safety` in the pack for irreversible plans.
- Hand cheap tight loops to Grok 4.6.

## Should not
- Load every skill or the PDF.
- Dump chapter notebooks into the 1M window.
- Skip `human-in-the-loop` when a human must approve.
- Spend frontier tokens on trivial routing.

## Starter pack
`planning`, `goal-setting`, `routing`, `prioritization`, `multi-agent`,
`reflection`, `reasoning-techniques`, `evaluation-monitoring`,
`guardrails-safety`, `resource-aware-optimization`.
