# Evaluation patterns (Ch 19)

Two notebooks: basic accuracy function, LLM-as-judge with Gemini.

Basic: `evaluate_response_accuracy(agent_output, expected_output) -> float` — normalized exact match (`strip().lower()`); example "capital of France" pair. Good as a smoke gate, not a quality bar.

LLM-as-judge: `genai.configure(api_key=os.environ['GOOGLE_API_KEY'])`, `logging INFO`, rubric prompt scoring open-ended outputs to JSON; wrap in typed function with `Optional` handling.

Monitoring rule: log `(version, prompt_hash, score, judge_model)` per run; alert on rolling-average drops; keep a golden set re-run per release.

## Notebook extracts (on-demand detail)

### Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb

```python
def evaluate_response_accuracy(agent_output: str, expected_output: str) -> float:
score = evaluate_response_accuracy(agent_response, ground_truth)
def timed_agent_action(agent_function, *args, **kwargs):
def simulated_tool_call(query):
class LLMInteractionMonitor:
def __init__(self):
def record_interaction(self, prompt: str, response: str):
def get_total_tokens(self):
# This is a very basic exact match; real-world would use more sophisticated metrics
# Example usage with a dummy agent function
```

### Chapter_19_Evaluation_(LLM_as_Judge).ipynb

```python
class LLMJudgeForLegalSurvey:
def __init__(self, model_name: str = 'gemini-1.5-flash-latest', temperature: float = 0.2):
def _generate_prompt(self, survey_question: str) -> str:
def judge_survey_question(self, survey_question: str) -> Optional[dict]:
import google.generativeai as genai
# Set your API key as an environment variable to run this script
# --- LLM-as-a-Judge Rubric for Legal Survey Quality ---
# Check for content moderation or other reasons for an empty response.
import os
import json
```
