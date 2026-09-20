# Goal Setting and Monitoring

Ch 11.

## Frameworks
- LangChain ChatOpenAI code agent; stdlib (re, pathlib) goal checkers.

## Key APIs from the notebooks
- `generate_prompt(...) builds goal-conditioned prompts`
- `get_code_feedback(code, goals) -> critique text; goals_met(feedback, goals) -> bool`
- `clean_code_block / to_snake_case / add_comment_header post-processors`

## Code patterns
- Pattern: state goals -> generate -> goals_met check -> targeted revise -> repeat (max 5).
- Goals as explicit strings (e.g. 'has unit tests', 'typed args').
- Persist each passing artifact with save_code_to_file.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_11_Goal_Setting_(Iteration).ipynb`

