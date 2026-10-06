# Stand-up path for a fresh agent

Given only this repo, do these five steps in order. Do not open the PDF.
Do not load every skill. The tables below are parsed by
`tools/standup_sim.py`, so keep their format.

Stand-up budget: 5000 tokens (cl100k), counting AGENTS.md, STANDUP.md, one
profile, manifest.json and the selected SKILL.md files. This number is
DERIVED, not from the book.

## Step 1: identify your runtime
Write one line naming your runtime and model, e.g. "Claude Code CLI",
"Grok 4.6 executor", "Muse personal agent". If you do not know, say "unknown".

## Step 2: load one profile
Lowercase that line. The first row with a matching signal (substring) wins.
`*` is the fallback. Load only that one profile.

| runtime signal | profile |
|---|---|
| muse | models/muse.md |
| fable 5.1, fable-5-1 | models/fable-5-1.md |
| grok 4.6, grok-4-6 | models/grok-4-6.md |
| codex, claude code, cursor, gemini cli, agy, coding agent, cli agent | models/coding-cli-agent.md |
| grok bot, desktop, chat assistant, personal assistant, browser agent | models/desktop-assistant-agent.md |
| * | models/desktop-assistant-agent.md |

Fallback rule: an unknown runtime gets the most conservative general
profile, which confirms before acting and keeps a small budget. Model specs
that a profile marks UNVERIFIED stay unverified. Do not fill them in.

## Step 3: read `manifest.json`
It holds one entry per skill (`id`, `chapter`, `role`, `when_to_use`,
`when_not_to_use`, `chains_with`, `token_cost_estimate`). The `role` column
below copies the manifest.

## Step 4: pick skills from the task (lazy-load)
1. Lowercase the task. A signal matches as a whole word or phrase, with an
   optional `s`, `es`, `d`, `ed` or `ing` suffix.
2. Every row with at least one match is a candidate. Safety rows come
   first, in table order. The rest follow, sorted by number of matched
   signals and then table order.
3. Load at most 3 `skills/<id>/SKILL.md`. With no match, load none and just
   do the task.
4. Load a `chains_with` skill only when its SKILL.md "Next skills" condition
   holds. Open `references/` only for implementation detail.

| skill id | role | task signals |
|---|---|---|
| human-in-the-loop | safety | on my behalf, send, email, pay, payment, purchase, buy, delete, irreversible, approve, approval, escalate, publish, transfer money, sign |
| guardrails | safety | guardrail, safety, unsafe, jailbreak, prompt injection, moderation, pii, content filter, policy, on my behalf |
| exception-handling | safety | fail, failure, error, retry, timeout, recover, fallback, crash, exception |
| prompt-chaining | executor | pipeline, multi-step, chain, stage, workflow |
| routing | planner, executor | route, classify, dispatch, triage, intent |
| parallelization | executor | parallel, concurrent, concurrently, fan out, simultaneous |
| reflection | critic | critique, self-review, refine, review my draft, revise |
| tool-use | executor | tool, function call, api, live data, external data |
| planning | planner | plan, planning, multi-step, decompose, research, roadmap |
| multi-agent | planner, executor | multi-agent, specialist, crew, team of agents, delegate |
| memory-management | memory | remember, memory, preference, session state, conversation history, long-term |
| learning-adaptation | memory, critic | learn from, self-improving, adapt, fine-tune, evolve |
| mcp | memory, executor | mcp, model context protocol, tool server |
| goal-setting | planner | goal, objective, success criteria, kpi, measurable |
| rag | memory | document, knowledge base, corpus, retrieve, retrieval, private data, vector, cite sources |
| a2a | executor, planner | a2a, agent card, remote agent, inter-agent, interoperate |
| resource-aware-optimization | planner | cost, cheap, cheaper model, latency, token budget, model tier |
| reasoning-techniques | critic | reasoning, chain of thought, tree of thought, react, logic puzzle, math |
| evaluation-monitoring | critic | evaluate, evaluation, metric, benchmark, monitor, drift, accuracy |
| prioritization | planner | prioritize, prioritise, priority, rank tasks, urgent, backlog |
| exploration-discovery | planner, critic | hypothesis, hypotheses, discover, novel idea, open-ended, scientific research |

## Step 5: self-check before acting
Answer all five. If you cannot, go back a step.
1. Profile: which `models/*.md` file did you load, and why?
2. Skills: which SKILL.md files did you load? There must be 3 or fewer per
   task, within your profile's cap.
3. Confirmation: before any send, pay, delete, share, publish or other
   irreversible action, you get an explicit APPROVE from a human. Silence
   or a timeout means denied.
4. Auth and guardrails: you never skip authentication, confirmation or
   guardrails. Secrets come from environment variables, never from files
   or prompts.
5. Labels: SOURCE means from the book. DERIVED means ours.
   EXTERNAL-UNVERIFIED, UNCERTAIN and UNVERIFIED mean unchecked: do not
   present them as fact.
