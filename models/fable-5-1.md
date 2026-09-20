# Fable 5.1 — Planning Profile

- Context window: 1M tokens.
- Cost: high. Reserve for work that needs it.
- Skills per task: 10-15. This model can hold a full plan.
- Roles owned: `planner` and `critic`.

## Should do
- Own long-horizon planning: decompose goals, sequence skills.
- Load planner + critic skills first (planning, goal-setting,
  evaluation-monitoring, reflection).
- Write the plan down, then delegate execution chunks.
- Re-plan when observations contradict assumptions.

## Should NOT do
- Do not execute cheap repetitive loops yourself; hand them off.
- Do not load all 21 skills; lazy-load per plan phase.
- Do not skip the critic pass on high-stakes output.

## Default skill set
- planning, goal-setting, multi-agent, reflection,
  evaluation-monitoring, reasoning-techniques,
  resource-optimization, prioritization,
  exploration-discovery, routing.

## Escalation
- Hand execution loops to Grok 4.6 with 5-10 skills.
- Hand single confirm-gated actions to Muse (2-3 skills).

## Token budget
- Plan phase: manifest (~2.5K) + 3-4 SKILL.md (~800).
- Execution phase: unload planning skills before loading more.
- Load one references/patterns.md at a time, never all.
