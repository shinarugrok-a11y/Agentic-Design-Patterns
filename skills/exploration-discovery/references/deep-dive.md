# Exploration and Discovery — deep dive

Source: Chapter 21 + `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb`
(excerpts from github.com/SamuelSchmidgall/AgentLaboratory).

## Rule of thumb (book)
Use in open-ended, complex or rapidly evolving domains where the solution
space is not fully defined: scientific research, market analysis, security
vulnerability discovery, creative generation, personalised education. The
goal is to surface "unknown unknowns", not optimise a known process.

## Google Co-Scientist architecture (book)
Supervisor coordinates asynchronous specialised agents:
- **Generation**: initial hypotheses via literature exploration and simulated debate.
- **Reflection**: peer-review for correctness, novelty, quality.
- **Ranking**: Elo-based tournament through simulated scientific debates.
- **Evolution**: refine top hypotheses (simplify, synthesise, unconventional reasoning).
- **Proximity**: cluster similar ideas (proximity graph) to map the landscape.
- **Meta-review**: synthesise insights across reviews; feed back to the loop.
Validated in drug repurposing (AML), liver-fibrosis targets and bacterial
gene-transfer mechanisms, with human scientists confirming hypotheses.

## Agent Laboratory roles (notebook)
Phases: literature review -> plan formulation -> data preparation ->
experimentation -> results interpretation -> report writing -> review.
Roles: PhD student, Postdoc, ML engineer, Software engineer, Professor,
Reviewers. Agents talk through dialogue; one directs, one executes.

### Reviewer ensemble with distinct personas
```python
class ReviewersAgent:
    def inference(self, plan, report):
        reviewer_1 = "You are a harsh but fair reviewer and expect good experiments that lead to insights for the research topic."
        reviewer_2 = "You are a harsh and critical but fair reviewer who is looking for an idea that would be impactful in the field."
        reviewer_3 = "You are a harsh but fair open-minded reviewer that is looking for novel ideas that have not been proposed before."
        return "\n".join(f"Reviewer #{i}:\n{get_score(outlined_plan=plan, latex=report, reward_model_llm=self.model, reviewer_type=r)}"
                         for i, r in enumerate([reviewer_1, reviewer_2, reviewer_3], 1))
```
### Structured review template (from Sakana AI Scientist)
```
Respond in the following format:

THOUGHT:
<THOUGHT>

REVIEW JSON:
```json
<JSON>
```

In <THOUGHT>, first briefly discuss your intuitions and reasoning for the evaluation. Be specific to the paper.
In <JSON>, provide the review with fields in order:
- "Summary", "Strengths" (list), "Weaknesses" (list)
- "Originality", "Quality", "Clarity", "Significance": 1-4 (low..very high)
- "Questions" (for authors), "Limitations" (incl. societal impact), "Ethical Concerns" (bool)
- "Soundness", "Presentation", "Contribution": 1-4 (poor..excellent)
- "Overall": 1-10 (very strong reject .. award quality)
- "Confidence": 1-5
- "Decision": "Accept" or "Reject" only.
This JSON will be automatically parsed, so ensure the format is precise.
```
`get_score` retries parsing up to `attempts=3`.

### Role prompts (director / executor pairs)
```
"You are a machine learning engineer being directed by a PhD student who will help you write the code,
and you can interact with them through dialogue. Your goal is to produce code that prepares the data for
the provided experiment. You should aim for simple code to prepare the data, not complex code..."

"You are a software engineer directing a machine learning engineer, where the machine learning engineer
will be writing the code, and you can interact with them through dialogue. Your goal is to help the ML
engineer produce code that prepares the data for the provided experiment..."
```
### Phase-scoped context (PostdocAgent)
```python
def context(self, phase):
    sr_str = (f"Previous Experiment code: {self.prev_results_code}\nPrevious Results: {self.prev_exp_results}\n"
              f"Previous Interpretation of results: {self.prev_interpretation}\nPrevious Report: {self.prev_report}\n"
              f"{self.reviewer_response}\n") if self.second_round else ""
    if phase == "plan formulation":
        return sr_str, f"Current Literature Review: {self.lit_review_sum}"
    if phase == "results interpretation":
        return sr_str, (f"Current Literature Review: {self.lit_review_sum}\nCurrent Plan: {self.plan}\n"
                        f"Current Dataset code: {self.dataset_code}\nCurrent Experiment code: {self.results_code}\n"
                        f"Current Results: {self.exp_results}")
```
Each agent receives only the artifacts relevant to its phase; second rounds
prepend prior results and reviewer feedback.

### Professor: final artifact
```python
sys_prompt = f"You are {self.role_description()} \n Here is the written paper \n{self.report}. Task instructions: Your goal is to integrate all of the knowledge, code, reports, and notes provided to you and generate a readme.md for a github repository."
```

## Generic discovery loop
```
hypotheses = generate(question, k)
loop rounds:
    reviews  = [review(h, persona) for h in hypotheses for persona in personas]
    ranked   = tournament(hypotheses, reviews)          # Elo / pairwise debate
    hypotheses = evolve(top(ranked, m)) + explore(new)  # exploit + explore
    if converged or budget spent: break
report(top(ranked))
```

## Checklist
- Diverse reviewer personas and models; check for groupthink.
- Separate "novel" from "correct" scores; both required to advance.
- Hard round/budget caps; log every hypothesis lineage.
- Safety/ethics gate before any experiment executes (`guardrails`, `human-in-the-loop`).

## Pattern variants
- **Generate–debate–evolve loop** — a bounded cycle of generation, critique, ranking, and refinement; the core loop of Google's AI co-scientist.
- **Role-specialized agents** — Generation, Reflection (peer review), Ranking, Evolution, Proximity (clusters similar ideas), and Meta-review (synthesizes recurring review patterns), under an async Supervisor.
- **Elo tournament ranking** — hypotheses compete pairwise in simulated debates; Elo gives a score comparable across rounds and a plateau to stop on.
- **Tripartite review panel** — three reviewer personas (insight-, impact-, novelty-focused) score the same artifact and their reviews are concatenated, not averaged away.
- **Phase pipeline** — literature review, experimentation, report writing, knowledge sharing (Agent Laboratory); each phase has its own agents and context.
- **Test-time compute scaling** — spend more inference iterating on the best hypotheses; quality tracks compute, so the budget is the tuning knob.
- **Scientist-in-the-loop** — the human sets the goal and steers the search; the system augments, not replaces.

## More prompt templates
Reviewer persona plus the structured verdict format (`get_score`):

```
You are a harsh but fair reviewer who expects experiments that yield real
insight for the research topic.
[persona 2: "...looking for an idea that would be impactful in the field";
 persona 3: "...open-minded, looking for novel ideas not proposed before"]

Respond in the following format:
THOUGHT: <specific intuitions about THIS work; not generic commentary>
REVIEW JSON: {"Summary":..., "Strengths":[...], "Weaknesses":[...],
  "Originality"|"Quality"|"Clarity"|"Significance"|"Soundness":1-4,
  "Questions":[...], "Limitations":[...], "Ethical Concerns":true|false,
  "Overall":1-10, "Confidence":1-5, "Decision":"Accept"|"Reject"}
Use only Accept or Reject - no borderline decisions. The JSON is parsed
automatically, so the format must be exact.
```

## Framework notes
- **Agent Laboratory** — `BaseAgent` subclasses (Professor, PostDoc, Reviewers, ML/SW Engineer), `max_steps` as the hard search bound, `query_model` for inference, AgentRxiv for sharing results across runs.
- **Google AI co-scientist** — Gemini-backed agents under a supervisor, Elo tournaments, safety review of both the research goal and each hypothesis.
- **LangChain / Google ADK** — not used in this chapter.

## Failure modes in depth
- **Unbounded search** — open-ended generation never terminates on its own; bound it with `max_steps`, a fixed number of rounds, an explicit compute budget, or an Elo plateau.
- **Untested hypotheses** — plausible prose scores well and means nothing; close the loop with an experiment phase that runs code or a wet-lab test, as the co-scientist's AML and liver-fibrosis results did.
- **Generator/reviewer collapse** — one critic carrying the generator's priors approves its own blind spots; use several distinct reviewer personas (ideally a different model), plus a meta-review to surface recurring weaknesses.
- **Irreversible actions** — exploration touching live systems does real damage; screen research goals and hypotheses on input, execute in a sandbox, and keep a human approving anything that leaves it.
