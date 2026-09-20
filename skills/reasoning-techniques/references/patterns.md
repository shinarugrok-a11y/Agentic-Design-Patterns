# Reasoning Techniques

Ch 17.

## Frameworks
- Google ADK (BuiltInCodeExecutor, google_search, agent_tool); CoT/self-correction prompt notebooks; DeepSearch.

## Key APIs from the notebooks
- `ADK: BuiltInCodeExecutor for verified computation; google_search for evidence`
- `CoT notebook: step-by-step prompt template`
- `Self_Correction notebook: answer -> verify -> correct loop`

## Code patterns
- Pattern: CoT trace -> extract answer -> verify (code/search) -> self-correct if needed.
- Keep traces internal; return concise answers.
- Sandbox all executed code.

## Prompt templates
- CoT: `Think step by step, then give the final answer on its own line: {problem}`
- Self-correct: `Verify each step above. If any step is wrong, redo from that step.`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_17_Reasoning_(CoT_Prompt).ipynb`
- `chapter_notebooks/Chapter_17_Reasoning_(Executing_Code).ipynb`
- `chapter_notebooks/Chapter_17_Reasoning_(Google_DeepSearch).ipynb`
- `chapter_notebooks/Chapter_17_Reasoning_(Self_Correction).ipynb`

