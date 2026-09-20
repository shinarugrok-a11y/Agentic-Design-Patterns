# Grok 4.6

## Profile
- Context window: ~500K tokens
- Cost: low
- Use for: execution loops and iteration
- Preferred skill count: 5–10 `SKILL.md` files
- Owns role: **executor**
- Do not use for planning

## Load order
1. `AGENTS.md`
2. `manifest.json`
3. Executor `SKILL.md` files only
4. `examples/minimal.py` plus one `references/patterns.md` for the skill in hand

## Should
- Implement `prompt-chaining`, `routing`, `parallelization`, `tool-use`, `mcp`.
- Always add `exception-handling` when tools or networks are involved.
- Iterate on failures; keep traces short.
- Stop and ask a planner (Fable) when the task needs a new strategy.

## Should not
- Own `planning`, `goal-setting`, or long-horizon `exploration-discovery`.
- Load the full critic stack unless the planner named those skills.
- Read the PDF or every notebook in a chapter.
- Convert tool errors into fluent excuses; flag and recover.

## Starter pack
`prompt-chaining`, `routing`, `tool-use`, `parallelization`,
`exception-handling`, and `mcp` when tools are remote.
