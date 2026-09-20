# Evaluation and Monitoring — Pattern reference

Load this file only when implementing `evaluation-monitoring`. Do not load by default.

## Book (Gulli) — rule of thumb
Use in production to score quality, latency, tokens, and goal progress; catch drift and anomalies.

## Book — visual (figure captions; images stay in the PDF)
Fig. 2: Contract execution among agents. Fig. 3: Evaluation support for Google ADK. Fig. 4: Evaluation and Monitoring design pattern.

## Notebooks (extracted)

Evaluation and Monitoring

### Notebooks
- `Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb`
- `Chapter_19_Evaluation_(LLM_as_Judge).ipynb`

### Patterns
- **Exact-match accuracy:** strip/lowercase comparison (baseline metric)
- **Latency monitoring:** `time.perf_counter()` wrapper around agent/tool calls
- **Token tracking:** placeholder word-count monitor (replace with real tokenizer)
- **LLM-as-judge:** rubric-based evaluation with `response_mime_type="application/json"`
- **Domain rubric:** 5 criteria × 1–5 for legal survey questions

### Prompt templates
Legal survey rubric (excerpt):
```
You are an expert legal survey methodologist and a critical legal reviewer. Your task is to evaluate the quality of a given legal survey question.

Provide a score from 1 to 5 for overall quality, along with a detailed rationale and specific feedback.
Focus on the following criteria:

1.  **Clarity & Precision (Score 1-5):**
...
5.  **Appropriateness for Audience (Score 1-5):**

**Output Format:**
Your response MUST be a JSON object with the following keys:
* `overall_score`, `rationale`, `detailed_feedback`, `concerns`, `recommended_action`
```

### Minimal code
```python
def evaluate_response_accuracy(agent_output: str, expected_output: str) -> float:
    return 1.0 if agent_output.strip().lower() == expected_output.strip().lower() else 0.0

def timed_agent_action(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, (time.perf_counter() - start) * 1000
```

```python
# LLM judge
response = model.generate_content(
    full_prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.2, response_mime_type="application/json"
    ),
)
return json.loads(response.text)
```

### Caveats
- Exact-match fails on paraphrased correct answers
- Token monitor uses `len(text.split())` — not real token counts
- LLM judge: empty `response.parts` may indicate safety block — check `prompt_feedback.safety_ratings`
- Requires `GOOGLE_API_KEY` for Gemini judge

---

## Failure modes (skill-level)
- Exact-match punishes valid paraphrases
- Word-count as token usage
- Judge JSON empty due to safety block

## Chains with
`reflection`, `goal-setting`
