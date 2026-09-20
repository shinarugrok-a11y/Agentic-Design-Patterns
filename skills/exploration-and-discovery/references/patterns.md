# Exploration and Discovery — Patterns

## Pattern variants
- **Generate–debate–evolve loop** — a bounded cycle of generation, critique, ranking, and refinement; the core loop of Google's AI co-scientist.
- **Role-specialized agents** — Generation, Reflection (peer review), Ranking, Evolution, Proximity (clusters similar ideas), and Meta-review (synthesizes recurring review patterns), under an async Supervisor.
- **Elo tournament ranking** — hypotheses compete pairwise in simulated debates; Elo gives a score comparable across rounds and a plateau to stop on.
- **Tripartite review panel** — three reviewer personas (insight-, impact-, novelty-focused) score the same artifact and their reviews are concatenated, not averaged away.
- **Phase pipeline** — literature review, experimentation, report writing, knowledge sharing (Agent Laboratory); each phase has its own agents and context.
- **Test-time compute scaling** — spend more inference iterating on the best hypotheses; quality tracks compute, so the budget is the tuning knob.
- **Scientist-in-the-loop** — the human sets the goal and steers the search; the system augments, not replaces.

## Prompt templates

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

## Code patterns

Agent Laboratory — one reviewer class, three independent personas over the same plan and report:

```python
class ReviewersAgent:
    def inference(self, plan, report):
        reviewer_1 = "You are a harsh but fair reviewer ... insights."
        review_1 = get_score(outlined_plan=plan, latex=report,
                             reward_model_llm=self.model, reviewer_type=reviewer_1)
        ...  # reviewer_2 impact-focused, reviewer_3 novelty-focused
        return f"Reviewer #1:\n{review_1}, \nReviewer #2:\n{review_2}, ..."
```

Agent Laboratory (phase-scoped roles) — each agent declares its phases and the context it sees, carrying the previous round forward:

```python
class PostdocAgent(BaseAgent):     # max_steps bounds the search
    phases = ["plan formulation", "results interpretation"]

    def context(self, phase):      # second round sees the prior round
        return f"Previous Results: {self.prev_exp_results}\n..."
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

## Source
Chapter 21 of "Agentic Design Patterns" (Gulli). Notebook: Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb.
