# Learning and Adaptation — Patterns

## Pattern variants
- **Self-modifying agent (SICA)** — agent rewrites its own codebase, picks the next parent from an archive of past versions scored on success/time/cost; wins when the agent's own tooling (editors, symbol lookup) is the bottleneck.
- **Evolutionary program search (AlphaEvolve, OpenEvolve)** — LLM ensemble proposes variants, an automated evaluator scores them, survivors seed the next round; wins when fitness is cheap to compute and the search space is large.
- **Reinforcement learning (PPO)** — clipped surrogate objective keeps each policy update inside a trust region; wins for continuous control where a reward signal exists and collapse must be avoided.
- **Preference optimization (DPO)** — optimizes the policy straight from preference pairs, skipping the separate reward model; wins for LLM alignment where reward hacking is the main risk.
- **Online / memory-based learning** — update from the live stream, or retrieve proven past solutions from a RAG knowledge base; wins when retraining is impossible mid-run.
- **Few-shot / in-context adaptation** — change behavior by changing examples only; wins when the change must be instant and reversible.

## Prompt templates

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

## Code patterns

OpenEvolve (evolutionary loop over whole files):
```python
from openevolve import OpenEvolve

evolve = OpenEvolve(
    initial_program_path="path/to/initial_program.py",
    evaluation_file="path/to/evaluator.py",   # fitness lives outside the evolved code
    config_path="path/to/config.yaml",
)
best_program = await evolve.run(iterations=1000)   # hard budget cap
for name, value in best_program.metrics.items():
    print(f"  {name}: {value:.4f}")
```

SICA (distilled: archive -> select -> self-modify -> re-benchmark):
```python
archive.append(Version(code=baseline, score=benchmark(baseline)))
for _ in range(META_ITERATIONS):
    parent = max(archive, key=lambda v: v.score)      # weighted success/time/cost
    child = parent.self_modify(archive)               # agent edits its own source
    archive.append(Version(code=child, score=benchmark(child)))
overseer.review(archive)   # async overseer LLM; can cancel on loops or stagnation
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

## Source
Chapter 9 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_09_Adaptation_(OpenEvolve).ipynb.
