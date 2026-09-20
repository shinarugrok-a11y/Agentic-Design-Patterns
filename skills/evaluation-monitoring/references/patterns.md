# Evaluation and Monitoring — reference patterns

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
