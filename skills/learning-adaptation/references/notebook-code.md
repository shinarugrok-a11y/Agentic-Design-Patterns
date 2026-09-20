# Learning and Adaptation — reference patterns

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
