# Learning and Adaptation — deep dive

Source: Chapter 9 + `Chapter_09_Adaptation_(OpenEvolve).ipynb`.
Note: this chapter's notebook is a single short snippet; most detail here is
from the chapter text.

## Rule of thumb (book)
Use when agents operate in dynamic, uncertain or evolving environments and
need personalisation, continuous improvement, or autonomous handling of novel
situations. "Adaptation" is the visible behaviour change produced by learning.

## Learning mechanisms catalogued
| Mechanism | Signal | Typical use |
|---|---|---|
| Reinforcement learning | reward/penalty | game play, robotics, trading |
| Supervised / few-shot | labelled examples | classification, tone |
| Unsupervised | structure in data | clustering user behaviour |
| Online learning | streaming updates | fraud, recommendations |
| Memory-based (RAG) | stored solutions | reuse of proven strategies (see `rag`, `memory-management`) |
| Self-modification (SICA) | benchmark score | agent edits its own code |
| Evolutionary (AlphaEvolve / OpenEvolve) | evaluator metrics | algorithm discovery |
| PPO / DPO | reward model / preference pairs | LLM alignment |

## OpenEvolve loop (notebook)
```python
from openevolve import OpenEvolve

evolve = OpenEvolve(
    initial_program_path="path/to/initial_program.py",
    evaluation_file="path/to/evaluator.py",     # returns metrics dict
    config_path="path/to/config.yaml")

best_program = await evolve.run(iterations=1000)
for name, value in best_program.metrics.items():
    print(f"  {name}: {value:.4f}")
```
Components you must supply: a seed program, an evaluator that scores any
candidate deterministically, and a config (LLM ensemble, population size,
mutation prompts).

## SICA self-improvement cycle (chapter)
1. Read archive of past agent versions and benchmark results.
2. Select best version by weighted utility (success, time, cost).
3. That version analyses the archive and edits its own codebase.
4. Benchmark the modified agent; append to archive. Repeat.
Emergent tools SICA built for itself: Smart Editor, Diff-Enhanced Editor,
AST Symbol Locator, Hybrid Symbol Locator. Architecture: sub-agents
(coding, problem-solving, reasoning) plus an asynchronous overseer that can
intervene; context window layout (system prompt, core prompt, assistant
messages) matters for efficiency.

## AlphaEvolve (chapter)
LLM ensemble (Gemini Flash for breadth, Pro for depth) proposes code
changes; automated evaluators score them; an evolutionary framework keeps
the best. Reported wins: matrix multiplication (4x4 complex, 48 scalar
mults), data-centre scheduling, TPU circuit design, kernel speedups.

## Minimal in-house loop
```python
archive = [(score(seed), seed)]
for _ in range(budget):
    parent = max(archive)[1]
    child = llm(f"Improve this program for {objective}. Return full code.\n{parent}")
    if compiles(child):
        archive.append((score(child), child))
best = max(archive)
```
Add a held-out evaluation before promoting `best`, or you will select on
noise/over-fitting to the evaluator.

## Guardrails for learning agents
- Evaluator must be automatic, deterministic and not gameable.
- Freeze safety-critical behaviour; learn only within a sandboxed scope.
- Keep the archive; roll back when metrics regress.
- Log every self-edit for audit (see `evaluation-monitoring`).

## Pattern variants
- **Self-modifying agent (SICA)** — agent rewrites its own codebase, picks the next parent from an archive of past versions scored on success/time/cost; wins when the agent's own tooling (editors, symbol lookup) is the bottleneck.
- **Evolutionary program search (AlphaEvolve, OpenEvolve)** — LLM ensemble proposes variants, an automated evaluator scores them, survivors seed the next round; wins when fitness is cheap to compute and the search space is large.
- **Reinforcement learning (PPO)** — clipped surrogate objective keeps each policy update inside a trust region; wins for continuous control where a reward signal exists and collapse must be avoided.
- **Preference optimization (DPO)** — optimizes the policy straight from preference pairs, skipping the separate reward model; wins for LLM alignment where reward hacking is the main risk.
- **Online / memory-based learning** — update from the live stream, or retrieve proven past solutions from a RAG knowledge base; wins when retraining is impossible mid-run.
- **Few-shot / in-context adaptation** — change behavior by changing examples only; wins when the change must be instant and reversible.

## More prompt templates
```
You are improving an agent. Here is the archive of past versions with their
benchmark scores (success rate, wall time, cost):
{archive_table}

Propose ONE novel, feasible modification to the current best version.
State: the file to change, the change, and the metric you expect it to move.
Do not propose a change you cannot evaluate on the existing benchmark.
```

```
Score this candidate against the held-out benchmark only.
Return JSON: {"success_rate": float, "seconds": float, "cost_usd": float}
Do not reward style, verbosity, or anything not in the benchmark.
```

## Framework notes
- **LangChain / LangGraph** — not used in this chapter; the adaptation loop is ordinary Python around whatever runner you already have.
- **Google ADK** — not used in this chapter.
- **OpenEvolve / SICA** — OpenEvolve's controller drives a program sampler, program database, evaluator pool, and LLM ensembles; SICA adds coding/problem-solver/reasoning sub-agents invoked like tools, Docker isolation, and a callgraph viewer.

## Failure modes in depth
- **Proxy metric diverges from the real goal** — a learned reward model gets hacked (high score, bad response). Keep fitness in a separate evaluator file, score a held-out human-rated slice, or use DPO on preference pairs instead of a reward-model judge.
- **Self-modification with no overseer or rollback** — the agent can break its own editor. Keep every version in the archive so any parent can be restored, run inside a container, and require the async overseer's review before a change is kept.
- **Overfitting to a small benchmark set** — variants tune to the cases they see. Score on a fixed held-out set that mutation cannot touch, and weight time and cost alongside success so verbose wins get penalized.
- **Unbounded evolution loops** — set an explicit `iterations=` cap, and let the overseer watch the callgraph for repeated work or stagnation and cancel execution.
