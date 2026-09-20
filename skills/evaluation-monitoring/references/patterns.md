# Evaluation and Monitoring

Ch 19.

## Frameworks
- Stdlib harnesses (time, logging); Gemini LLM-judge class.

## Key APIs from the notebooks
- `evaluate_response_accuracy(agent_output, expected_output) -> float`
- `timed_agent_action(fn, *args) latency wrapper; simulated_tool_call(query) fixture`
- `LLMInteractionMonitor: record_interaction / get_total_tokens live tracking`

## Code patterns
- Pattern: offline eval (accuracy + judge) -> ship -> live monitor (tokens/latency/errors) -> alert.
- Pin a baseline before comparing versions.
- Log prompt+response pairs for judge audits.

## Prompt templates
- Judge: `Rubric: {rubric}. Score 0-5 and justify in one line: {output}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb`
- `chapter_notebooks/Chapter_19_Evaluation_(LLM_as_Judge).ipynb`

