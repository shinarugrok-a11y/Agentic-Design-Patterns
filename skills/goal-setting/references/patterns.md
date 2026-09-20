# Goal Setting patterns (Ch 11)

One notebook: iterative goal-tracking loop (MIT-licensed sample by Mahtab Syed; `langchain_openai`, `python-dotenv`).

Pattern: define goal with numeric target + deadline; loop `act -> measure -> compare`; each iteration logs delta vs target and decides continue/pivot/stop. `!pip install langchain_openai openai python-dotenv`; keys via `.env`.

Prompt templates: goal prompt forces SMART format (specific, measurable, deadline); check-in prompt asks for metric value, delta, blocker, next action — no prose without numbers.

Rule: every goal needs a stop condition (target met OR max iterations OR stall limit) to prevent endless iteration.

## Notebook extracts (on-demand detail)

### Chapter_11_Goal_Setting_(Iteration).ipynb

```python
def generate_prompt(
def get_code_feedback(code: str, goals: list[str]) -> str:
def goals_met(feedback_text: str, goals: list[str]) -> bool:
def clean_code_block(code: str) -> str:
def add_comment_header(code: str, use_case: str) -> str:
def to_snake_case(text: str) -> str:
def save_code_to_file(code: str, use_case: str) -> str:
def run_code_agent(use_case: str, goals_input: str, max_iterations: int = 5) -> str:
# https://www.linkedin.com/in/mahtabsyed/
# Permission is hereby granted, free of charge, to any person obtaining a copy
```
