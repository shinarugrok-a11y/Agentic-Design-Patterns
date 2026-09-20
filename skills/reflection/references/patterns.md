# Reflection

Ch 4.

## Frameworks
- Google ADK (SequentialAgent + LlmAgent critic); LangChain (generator chain + critic chain, async).

## Key APIs from the notebooks
- `ADK SequentialAgent: generator agent -> critic agent pipeline`
- `Iterative loop notebook: run_reflection_loop() with SystemMessage/HumanMessage critic turn`
- `LangChain notebook: run_reflection_example(product_details) generator-then-critique chains`

## Code patterns
- Pattern: draft -> critique against rubric -> revise -> repeat until PASS or max iters.
- Separate the critic prompt from the generator prompt; give the critic the rubric only.
- Cap at 2-4 iterations; keep every draft for audit.

## Prompt templates
- Critic: `Critique this draft against {rubric}. Reply PASS or FAIL + notes: {draft}`
- Revise: `Revise the draft using these notes, keep what works: {notes} \n {draft}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_04_Reflection_(ADK).ipynb`
- `chapter_notebooks/Chapter_04_Reflection_(Iterative_Loop).ipynb`
- `chapter_notebooks/Chapter_04_Reflection_(LangChain).ipynb`

