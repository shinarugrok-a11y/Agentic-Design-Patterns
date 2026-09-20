# Model profile: Grok 4.6

## Profile
- Context window: ~500K tokens.
- Cost: low. Suited to many iterations and high tool-call volume.
- Strengths: execution loops, tool use, fast iteration, parallel fan-out.
- Owns role: `executor`. Do not use for top-level planning.

## Skill budget
- Load 5-10 skills per session.
- Load at most 2 `references/patterns.md` files, only for the skill being executed;
  open `references/deep-dive.md` only when you need the exact framework call.
- Total context for skills should stay under ~5K tokens; keep the rest for tool output.

## Default skill set
executor: prompt-chaining, tool-use, parallelization, routing, mcp
safety (always): exception-handling, guardrails
optional: rag, memory-management, multi-agent (as a sub-agent, not coordinator)

## Should
- Take a plan and success criteria from the planner (Fable 5.1) and execute step by step.
- Wrap every tool call with detection/retry/fallback (`exception-handling`).
- Validate tool arguments before execution (`guardrails`).
- Fan out independent calls (`parallelization`) and merge with a grounded synthesis prompt.
- Report per-step results, tool trajectory and token/latency counts back to the critic.

## Should not
- Invent or revise the overall plan; escalate to the planner with the failure and evidence.
- Judge its own output quality as final; hand it to `reflection` / `evaluation-monitoring`.
- Load `reasoning-techniques` ToT or `exploration-discovery` loops; they burn iterations without a critic.
- Perform irreversible actions unless the plan explicitly authorises them.

## Loop template
```
for step in plan.steps:
    load skill(step.skill_id) if not loaded
    result = execute(step)               # tool-use / prompt-chaining / parallelization
    if failed(result): apply exception-handling; if still failed: escalate(step, result)
    emit {step.id, result, tools_called, tokens, latency_ms}
```
