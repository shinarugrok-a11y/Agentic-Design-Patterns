# Fable 5.1

## Profile
- Context window: ~1M tokens.
- Cost: high per token. Every call should earn its price.
- Strengths: long-horizon planning, holding a large problem in one context, critique.
- Best fit: multi-hour agentic work, architecture decisions, reviewing other agents' output.

## Skill budget
- Load 10-15 skills. At ~375 tokens per SKILL.md that is 4-6k tokens, negligible here.
- Load `references/patterns.md` freely for the skills you are actively applying.
- Reading `manifest.json` in full is fine at this context size; do not bother slicing by role.

## Owns
- `planner` role: `planning`, `goal-setting-and-monitoring`, `prioritization`,
  `resource-aware-optimization`, `multi-agent-collaboration`, `exploration-and-discovery`.
- `critic` role: `reflection`, `reasoning-techniques`, `evaluation-and-monitoring`,
  `learning-and-adaptation`.

## Do
- Decompose the goal first with `planning`, then hand concrete steps to a cheaper executor.
- Define success criteria up front with `goal-setting-and-monitoring` so the executor can
  self-check without calling back to you.
- Act as the separate critic in `reflection` and the judge in `evaluation-and-monitoring`.
  Do not let the executor grade its own work.
- Use `resource-aware-optimization` to decide which steps belong on Grok 4.6 instead of here.
- Write the plan down as data (step list with dependencies and done-when conditions) so
  execution can resume without replaying your reasoning.

## Do not
- Do not run tight execution loops here. Retry, poll, and iterate belong on Grok 4.6.
- Do not use this model for bulk transformation, formatting, or file-by-file edits.
- Do not re-read the whole manifest on every turn just because the context allows it.
- Do not plan past the point of diminishing returns; a plan the executor cannot act on is
  a plan that has to be rewritten.

## Handoff
- Down to Grok 4.6: ordered steps, per-step done-when criteria, the executor skills to load.
- Down to Muse: only steps that are safe to propose to a human, with confirmation required.
- Up from either: failure reports and trajectories, for `reflection` and replanning.
