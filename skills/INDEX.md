# Skill index

Generated from `manifest.json` by `python3 tools/validate.py --sync`; do not edit.

Pick rule: lowercase the task. A signal matches as a whole word or phrase, plus an optional s, es, d, ed or ing. Every row with a match is a candidate: safety rows first in table order, then the rest by most matches, then table order. Load at most 3 `skills/<id>/SKILL.md`; none if nothing matches. Load a `chains_with` skill only when its "Next skills" condition holds.

| id | role | use when | signals |
|---|---|---|---|
| prompt-chaining | executor | Chain prompts when each stage feeds the next. | pipeline, multi-step, chain, stage, workflow |
| routing | planner, executor | Classify a request, dispatch one handler. | route, classify, dispatch, triage, intent |
| parallelization | executor | Run independent branches concurrently, then merge. | parallel, concurrent, concurrently, fan out, simultaneous |
| reflection | critic | Critique a draft, refine until criteria pass. | critique, self-review, refine, review my draft, revise |
| tool-use | executor | Call typed functions for live data or actions. | tool, function call, api, live data, external data |
| planning | planner | Decompose a goal into ordered steps first. | plan, planning, multi-step, decompose, research, roadmap |
| multi-agent | planner, executor | Split work across specialist agents. | multi-agent, specialist, crew, team of agents, delegate |
| memory-management | memory | Keep session state and searchable long-term memory. | remember, memory, preference, session state, conversation history, long-term |
| learning-adaptation | memory, critic | Improve behaviour from scored outcomes. | learn from, self-improving, adapt, fine-tune, evolve |
| mcp | memory, executor | Discover tools via an MCP server. | mcp, model context protocol, tool server |
| goal-setting | planner | Define measurable goals, loop until judged met. | goal, objective, success criteria, kpi, measurable |
| exception-handling | safety | Retry transient failures, fall back, escalate. | fail, failure, error, retry, timeout, recover, fallback, crash, exception |
| human-in-the-loop | safety | Human confirmation at high stakes. | on my behalf, send, email, pay, payment, purchase, buy, delete, irreversible, approve, approval, escalate, publish, transfer money, sign |
| rag | memory | Retrieve top-k chunks, ground the answer. | document, knowledge base, corpus, retrieve, retrieval, private data, vector, cite sources |
| a2a | executor, planner | Delegate to remote agents via Agent Cards. | a2a, agent card, remote agent, inter-agent, interoperate |
| resource-aware-optimization | planner | Route to the cheapest adequate model or path. | cost, cheap, cheaper model, latency, token budget, model tier |
| reasoning-techniques | critic | Explicit reasoning: CoT, ToT, ReAct. | reasoning, chain of thought, tree of thought, react, logic puzzle, math |
| guardrails | safety | Screen inputs, tool args, outputs against policy. | guardrail, safety, unsafe, jailbreak, prompt injection, moderation, pii, content filter, policy, on my behalf |
| evaluation-monitoring | critic | Score accuracy, latency, cost with rubrics. | evaluate, evaluation, metric, benchmark, monitor, drift, accuracy |
| prioritization | planner | Rank tasks by urgency, importance, deps, cost. | prioritize, prioritise, priority, rank tasks, urgent, backlog |
| exploration-discovery | planner, critic | Generate, review, rank, evolve hypotheses. | hypothesis, hypotheses, discover, novel idea, open-ended, scientific research |
