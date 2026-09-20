# Grok 4.6 — Execution Profile

- Context window: 500K tokens.
- Cost: low. Built for execution loops and iteration.
- Skills per task: 5-10. Load only the current phase.
- Roles owned: `executor`. Do not use for planning.

## Should do
- Own execution loops: run tools, iterate, report back.
- Load executor skills for the assigned phase only
  (tool-use, prompt-chaining, parallelization, mcp, a2a).
- Retry with backoff; flag degraded fallbacks explicitly.
- Return a short trace: what ran, what failed, what is next.

## Should NOT do
- Do not plan multi-phase work; ask Fable 5.1 for a plan.
- Do not load planner/critic libraries speculatively.
- Do not take irreversible actions without confirmation.

## Default skill set
- tool-use, prompt-chaining, parallelization,
  multi-agent, routing, mcp, exception-handling.

## Escalation
- Push plan questions up to Fable 5.1.
- Push approvals and sends to Muse (human-in-the-loop).

## Token budget
- Work phase: manifest (~2.5K) + assigned SKILL.md files only.
- Unload finished phases before loading the next skill.
- Load references/patterns.md only when the SKILL.md is unclear.
