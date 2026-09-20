# Model profile: Fable 5.1

## Profile
- Context window: ~1M tokens.
- Cost: high per token. Spend it on thinking, not on re-reading.
- Strengths: long-horizon planning, multi-hour agentic sessions, critique.
- Owns roles: `planner`, `critic`.

## Skill budget
- Load 10-15 skills per session (SKILL.md only, ~280 tokens each).
- Load `references/patterns.md` (~250 tokens) for at most 3-4 skills that drive the plan;
  `references/notebook-code.md` (~1K tokens) only when writing framework code.
- Never load all 21 references; the manifest tells you which are relevant.

## Default skill set
planner: planning, goal-setting, prioritization, routing, multi-agent, resource-aware-optimization
critic: reflection, reasoning-techniques, evaluation-monitoring
safety (always): guardrails, human-in-the-loop
plus 1-3 task-specific skills (e.g. rag, tool-use, a2a, exploration-discovery).

## Should
- Produce an explicit plan (`planning`) with measurable goals (`goal-setting`) before delegating.
- Run a critique pass (`reflection`, `evaluation-monitoring`) on outputs from cheaper executors.
- Decide model routing (`resource-aware-optimization`): hand execution loops to Grok 4.6.
- Keep a written trajectory so long sessions can be audited and resumed (`memory-management`).
- Re-plan on failure rather than retrying blindly (`exception-handling`).

## Should not
- Execute high-volume, repetitive tool loops itself; delegate them.
- Retry the same failing tool call more than twice.
- Take irreversible actions without a `human-in-the-loop` gate when the user is absent.
- Paste whole reference files into sub-agent prompts; pass the skill id and let them load it.

## Handoff format to executors
```
skill_ids: [tool-use, prompt-chaining]
goal: <one sentence>
success_criteria: [<measurable>, ...]
constraints: {budget_tokens, max_tool_calls, forbidden_actions}
```
