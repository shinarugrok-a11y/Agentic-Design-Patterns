# Learning and Adaptation

Ch 9.

## Frameworks
- OpenEvolve (evolutionary program/prompt search).

## Key APIs from the notebooks
- `from openevolve import OpenEvolve; evolve loop over candidate programs with fitness scores`
- `14-line notebook: minimal evolve harness — candidate generation + selection`

## Code patterns
- Pattern: candidate -> fitness score -> select -> mutate -> repeat.
- Keep an elite archive; never lose the best-known policy.
- Fix the fitness function before scaling iterations.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_09_Adaptation_(OpenEvolve).ipynb`

