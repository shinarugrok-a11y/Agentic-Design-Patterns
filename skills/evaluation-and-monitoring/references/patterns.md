# Evaluation and Monitoring — Patterns

## Pattern variants
- **Response scoring** — compare the final answer to ground truth; exact match is the floor, cheap and brittle.
- **Trajectory evaluation** — compare the actual tool-call sequence to the ideal one via exact match, in-order match (extra steps allowed), any-order match, precision, recall, or single-tool use. Exact for high-stakes, in-order for flexible flows.
- **LLM-as-a-judge** — rubric-scored grading for qualities no string metric captures (clarity, neutrality, helpfulness).
- **Operational monitoring** — latency per action and input/output token counts recorded on every run, in dev and in production.
- **A/B comparison** — run two agent versions, models, or planners over the same evalset and diff the metric tables.
- **Drift and anomaly detection** — score against a stored baseline to catch concept drift and unexpected actions after deployment.
- **Multi-agent evaluation** — also score handoff correctness, plan adherence, agent selection, and whether adding an agent helps.

## Prompt templates

LLM-as-a-judge rubric (shape of `LEGAL_SURVEY_RUBRIC`); run at `temperature=0.2` or lower:

```
You are an expert <domain> reviewer. Evaluate the <artifact> below.
Score each criterion 1-5 (1 = <worst case>, 3 = <adequate>, 5 = <ideal>):
1. Clarity & precision   2. Neutrality & bias   3. Relevance & focus
4. Completeness          5. Appropriateness for audience
Your response MUST be a JSON object with the keys: overall_score (int 1-5),
rationale, detailed_feedback (one bullet per criterion with a concrete
improvement), concerns (list), recommended_action ("Revise for neutrality" |
"Approve as is" | "Clarify scope").
---
<ARTIFACT TO EVALUATE>
```

## Code patterns

Plain Python — the three base metrics:

```python
def evaluate_response_accuracy(agent_output: str, expected: str) -> float:
    return 1.0 if agent_output.strip().lower() == expected.strip().lower() else 0.0

def timed_agent_action(agent_function, *args, **kwargs):
    start = time.perf_counter()
    result = agent_function(*args, **kwargs)
    return result, (time.perf_counter() - start) * 1000      # latency_ms

class LLMInteractionMonitor:   # running input/output token totals per call
    def record_interaction(self, prompt, response): ...
```

Google ADK — the same evalset from pytest or the build pipeline:

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

await AgentEvaluator.evaluate(agent_module="home_agent",
                              eval_dataset_file_path_or_dir="tests/home.test.json")
# CLI equivalent: adk eval home_agent tests/home.evalset.json
```

## Framework notes
- **Google ADK** — `adk web` records sessions into an evalset, `AgentEvaluator.evaluate` runs under pytest in CI, `adk eval` runs in builds. A one-session `.test.json` unit-tests development; a multi-session `.evalset.json` covers integration. Each turn declares query, expected tool trajectory, and reference response; criteria live in `test_config.json`.
- **google-generativeai** — the judge is a `GenerativeModel` given the rubric and asked for JSON; catch `json.JSONDecodeError` and empty responses.
- **LangChain / LangGraph** — not used here; attach the same metric functions to the chain's callbacks.

## Failure modes in depth
- **Only final answers scored** — a right answer reached by a wrong path still passes; capture the trajectory and diff it against ground-truth tool calls.
- **Judge inherits generator bias** — same model family, same blind spots; use a different (often smaller) judge model, a written rubric rather than a holistic score, and several reviewer personas.
- **Metrics stop tracking value** — exact match rewards phrasing, not correctness ("Paris is the capital of France" scores 0.0 against "The capital of France is Paris"); pair it with rubric scoring and refresh test cases as the environment shifts.
- **Drift undetected** — no baseline means nothing to compare against; persist per-case scores, latency, and token counts each release and alert on the delta.

## Source
Chapter 19 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb, Chapter_19_Evaluation_(LLM_as_Judge).ipynb.
