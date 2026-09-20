# Evaluation and Monitoring — deep dive

Source: Chapter 19 + `Chapter_19_Evaluation_(Basic_Response_Evaluation)`,
`Chapter_19_Evaluation_(LLM_as_Judge)`.

## Why (book)
Agents are probabilistic and operate in changing environments; traditional
tests are insufficient. Needed: continuous assessment of effectiveness,
efficiency and adherence to operational/safety requirements; detection of
data drift, unexpected tool interactions and goal deviation; evaluation of
collaborative success in multi-agent systems. Evolving idea: agents as
"contractors" bound by formal, verifiable contracts (deliverables, scope,
negotiation, self-validation).

Rule of thumb: production agents where reliability matters; A/B comparison
of versions; regulated/high-stakes domains; drift-prone environments;
evaluating trajectories and subjective qualities.

## Metric layers
| Layer | Metric | Notebook snippet |
|---|---|---|
| Accuracy | exact/semantic match vs ground truth | `evaluate_response_accuracy` |
| Latency | ms per action | `timed_agent_action` |
| Cost | input/output tokens | `LLMInteractionMonitor` |
| Trajectory | actions taken vs ideal path | ADK evalsets |
| Quality | rubric score by LLM judge | `LLMJudgeForLegalSurvey` |

### Basic snippets
```python
def evaluate_response_accuracy(agent_output: str, expected_output: str) -> float:
    return 1.0 if agent_output.strip().lower() == expected_output.strip().lower() else 0.0
# "The capital of France is Paris." vs "Paris is the capital of France." -> 0.0  (exact match is too strict)

def timed_agent_action(agent_function, *args, **kwargs):
    start = time.perf_counter(); result = agent_function(*args, **kwargs)
    latency_ms = (time.perf_counter() - start) * 1000
    return result, latency_ms

class LLMInteractionMonitor:
    def __init__(self): self.total_input_tokens = 0; self.total_output_tokens = 0
    def record_interaction(self, prompt, response):
        self.total_input_tokens += len(prompt.split())     # placeholder: use the provider's token counter
        self.total_output_tokens += len(response.split())
```

## LLM-as-a-Judge (rubric)
```
You are an expert legal survey methodologist and a critical legal reviewer. Evaluate the quality of a given legal survey question.
Provide a score from 1 to 5 for overall quality, along with a detailed rationale and specific feedback.
1.  **Clarity & Precision (1-5)**   1: vague/ambiguous ... 5: perfectly clear and precise.
2.  **Neutrality & Bias (1-5)**     1: highly leading ... 5: completely neutral.
3.  **Relevance & Focus (1-5)**     1: irrelevant ... 5: directly relevant, single concept.
4.  **Completeness (1-5)**          1: omits critical info ... 5: all necessary context.
5.  **Appropriateness for Audience (1-5)**  1: inaccessible jargon / too simple ... 5: tailored.
**Output Format:** JSON with keys `overall_score` (int 1-5), `rationale`, `detailed_feedback` (per criterion),
`concerns` (legal/ethical/methodological), `recommended_action` ("Revise for neutrality", "Approve as is", "Clarify scope").
```
```python
class LLMJudgeForLegalSurvey:
    def __init__(self, model_name="gemini-1.5-flash-latest", temperature=0.2):   # low temp for consistency
        self.model = genai.GenerativeModel(model_name); self.temperature = temperature
    def judge_survey_question(self, survey_question: str) -> Optional[dict]:
        prompt = f"{LEGAL_SURVEY_RUBRIC}\n\n---\n**LEGAL SURVEY QUESTION TO EVALUATE:**\n{survey_question}\n---"
        response = self.model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
            temperature=self.temperature, response_mime_type="application/json"))
        if not response.parts:               # blocked by safety filters
            logging.error(response.prompt_feedback.safety_ratings); return None
        return json.loads(response.text)
```
Test set in the notebook: a well-formed Likert question (good), a leading
"Don't you agree that..." question (biased), "What are your thoughts on
legal tech?" (vague).

## ADK evaluation tooling (book)
- Test files (single session, unit-level) and evalset files (multi-session
  integration) define expected behaviour incl. tool trajectories.
- Run via web UI (interactive), `pytest` (CI/CD) or CLI.

## Trajectory evaluation
Compare the sequence of tool calls/decisions with a reference path:
exact match, in-order match, any-order match, precision/recall of tools
used. A correct final answer reached by a wasteful or unsafe trajectory
should still fail.

## Monitoring in production
Dashboards for latency, token cost, error rate, guardrail blocks,
escalation rate; alerts on drift; sampled LLM-judge scoring; A/B routing of
versions. Feed results to `reflection` (per-output) and
`learning-adaptation` (per-version).

## Checklist
- Use semantic or rubric scoring for natural-language answers.
- Calibrate the judge against a small human-labelled set.
- Log trajectories, not just answers.
- Track tokens with the provider's counter, not `split()`.

## Pattern variants
- **Response scoring** — compare the final answer to ground truth; exact match is the floor, cheap and brittle.
- **Trajectory evaluation** — compare the actual tool-call sequence to the ideal one via exact match, in-order match (extra steps allowed), any-order match, precision, recall, or single-tool use. Exact for high-stakes, in-order for flexible flows.
- **LLM-as-a-judge** — rubric-scored grading for qualities no string metric captures (clarity, neutrality, helpfulness).
- **Operational monitoring** — latency per action and input/output token counts recorded on every run, in dev and in production.
- **A/B comparison** — run two agent versions, models, or planners over the same evalset and diff the metric tables.
- **Drift and anomaly detection** — score against a stored baseline to catch concept drift and unexpected actions after deployment.
- **Multi-agent evaluation** — also score handoff correctness, plan adherence, agent selection, and whether adding an agent helps.

## More prompt templates
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

## Framework notes
- **Google ADK** — `adk web` records sessions into an evalset, `AgentEvaluator.evaluate` runs under pytest in CI, `adk eval` runs in builds. A one-session `.test.json` unit-tests development; a multi-session `.evalset.json` covers integration. Each turn declares query, expected tool trajectory, and reference response; criteria live in `test_config.json`.
- **google-generativeai** — the judge is a `GenerativeModel` given the rubric and asked for JSON; catch `json.JSONDecodeError` and empty responses.
- **LangChain / LangGraph** — not used here; attach the same metric functions to the chain's callbacks.

## Failure modes in depth
- **Only final answers scored** — a right answer reached by a wrong path still passes; capture the trajectory and diff it against ground-truth tool calls.
- **Judge inherits generator bias** — same model family, same blind spots; use a different (often smaller) judge model, a written rubric rather than a holistic score, and several reviewer personas.
- **Metrics stop tracking value** — exact match rewards phrasing, not correctness ("Paris is the capital of France" scores 0.0 against "The capital of France is Paris"); pair it with rubric scoring and refresh test cases as the environment shifts.
- **Drift undetected** — no baseline means nothing to compare against; persist per-case scores, latency, and token counts each release and alert on the delta.
