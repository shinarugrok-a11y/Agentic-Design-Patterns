# Learning patterns (Ch 9)

One notebook: OpenEvolve evolutionary loop.

Pattern: `OpenEvolve(initial_program_path, evaluation_file, config_path)` then `await evolve.run(iterations=1000)`; each iteration mutates the program, scores via evaluator, keeps winners. Report `best_program.metrics` per metric name.

Config (`config.yaml`): population size, mutation operators, elite archive, stop conditions. Evaluator file must be deterministic and fast (it runs 1000x).

Production rules: separate train vs held-out evaluators; archive elites and re-test top-K before promotion; require a review gate before deploying an evolved program.

## Notebook extracts (on-demand detail)

### Chapter_09_Adaptation_(OpenEvolve).ipynb

```python
evolve = OpenEvolve(
from openevolve import OpenEvolve
```
