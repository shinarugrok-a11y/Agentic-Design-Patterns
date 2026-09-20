# Fable 5.1 — Model Profile

- Context window: 1M tokens.
- Cost: high. Reserve for planning and long-horizon work.
- Load 10-15 skills per task.
- Owns `planner` and `critic` roles by default.

## Should
- Own decomposition: `planning`, `goal-setting`, `prioritization`.
- Run critique loops: `reflection`, `evaluation-monitoring`.
- Coordinate teams via `multi-agent` and `inter-agent-a2a`.
- Plan multi-hour agentic runs; checkpoint via `memory-management`.
- Reason explicitly with `reasoning-techniques` before committing.
- Explore open questions with `exploration-discovery` + reviewers.

## Should NOT
- Burn context on cheap execution loops; delegate to Grok 4.6.
- Load all 21 skills; lazy-load from `manifest.json`.
- Execute irreversible actions; hand `executor` steps to Grok 4.6
  and `safety` steps to Muse review.
- Skip evaluation baselines before declaring a plan successful.

## Default skill set
- planning, goal-setting, prioritization, reflection,
- evaluation-monitoring, multi-agent, exploration-discovery,
- reasoning-techniques, resource-optimization, memory-management.

## Token budget
- Planning pass: 1-2 skills (plan + goals).
- Critique pass: add `reflection` or `evaluation-monitoring`.
- Coordination: add `multi-agent` only when delegating.
- Stay under ~4000 tokens of skill text per run.

## Handoff protocol
- Write the step plan; assign executor steps to Grok 4.6.
- Attach success criteria so executors know when to stop.
- Route safety-role checks to Muse before irreversible steps.
- Replan from the failed step; never restart blindly.

## Routing
- Read `manifest.json`, pick planner/critic skills first.
- Escalate safety-role skills to Muse; execution to Grok 4.6.
