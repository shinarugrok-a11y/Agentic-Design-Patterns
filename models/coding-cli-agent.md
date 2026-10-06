# Runtime profile: coding CLI agent (Codex, Claude Code, Cursor, Gemini CLI / agy)

## Profile
- Runtime: an agent in a terminal or IDE with file read/write and shell access.
- Context window: unknown. It varies by model, plan and runtime, so check yours.
- Cost: unknown. Read only what the task needs.
- Strengths: reading repos, editing files, running `python3` locally.
- Roles: `executor` by default; `planner` for multi-file changes.

## Skill budget
- At most 3 SKILL.md per task (AGENTS.md boot step 4). Open `references/patterns.md`
  only for the skill you are implementing.
- Open `references/deep-dive.md` only when writing framework code. Check its
  `Provenance:` labels before copying anything.
- Use `ground-truth/` slices only when a citation or exact wording matters.

## Default skill set
always: exception-handling, guardrails
by task: tool-use, prompt-chaining, mcp, reflection, evaluation-monitoring

## Should
- Run `python3 tools/validate.py` after changing skills or the manifest.
- Run a skill's `examples/minimal.py` before copying its pattern; all run offline.
- Read API keys from environment variables and fail with a clear message if
  one is missing. Never hardcode keys or write them to files.
- Treat code marked DERIVED or ILLUSTRATIVE as ours. Only SOURCE blocks came
  from the book.
- Ask before destructive commands (deleting files, force-pushing, dropping data).

## Should not
- Load every skill or the PDF to "get context".
- Present DERIVED code as book code, or UNVERIFIED claims as fact.
- Skip auth, confirmation prompts, hooks or guardrails to finish faster.
- Modify `Agentic_Design_Patterns_Complete.pdf` or `chapter_notebooks/*.ipynb`.
- Retry a failing command more than twice without changing something.

## Task note format
```
runtime: <name>   profile: models/coding-cli-agent.md
skills: [<id>, ...] (<= 3)
plan: <one line>   checks: python3 tools/validate.py
```
