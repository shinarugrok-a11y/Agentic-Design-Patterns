# Learning and Adaptation — Pattern reference

Load this file only when implementing `learning-and-adaptation`. Do not load by default.

## Book (Gulli) — rule of thumb
Use for agents in changing environments that must personalize, improve from traces, or handle novel cases.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: SICA self-improvement. Fig. 3: OpenEvolve controller. Fig. 4: Learning and adapting pattern.

## Notebooks (extracted)

Learning and Adaptation

### Notebooks
- `Chapter_09_Adaptation_(OpenEvolve).ipynb`

### Patterns
- **OpenEvolve:** evolutionary program improvement via `initial_program_path`, `evaluation_file`, `config_path`
- **Async execution:** `await evolve.run(iterations=N)` returns best program with metrics

### Prompt templates
None in notebook.

### Minimal code
```python
from openevolve import OpenEvolve

evolve = OpenEvolve(
    initial_program_path="path/to/initial_program.py",
    evaluation_file="path/to/evaluator.py",
    config_path="path/to/config.yaml",
)
best_program = await evolve.run(iterations=1000)
print(best_program.metrics)
```

### Caveats
- **Thin notebook** — stub only; requires external program, evaluator, and config files
- Async context required (`await`)
- No markdown documentation in notebook

---

## Failure modes (skill-level)
- Reward hacking the evaluator
- Unconstrained self-modification
- No baseline so 'better' is undefined

## Chains with
`reflection`, `memory-management`
