# Exploration and Discovery — Pattern reference

Load this file only when implementing `exploration-discovery`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when the agent must seek unknown unknowns (literature, hypotheses, experiments), not just answer a known query.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: AI Co-Scientist ideation to validation. Fig. 2: Exploration and Discovery design pattern.

## Notebooks (extracted)

Exploration and Discovery

### Notebooks
- `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb`

### Patterns
- **Agent Laboratory pattern:** multi-role research pipeline (Postdoc, Professor, Reviewers)
- **Multi-reviewer scoring:** 3 independent reviewer personas → structured JSON review
- **Phased agents:** `self.phases` lists workflow stages; `context(phase)` builds state-specific prompts
- **Review template:** THOUGHT + REVIEW JSON with Originality/Quality/Clarity/Significance/Decision fields
- **Human-in-loop analogue:** iterative review/refinement before publication

### Prompt templates
Reviewer personas:
```
You are a harsh but fair reviewer and expect good experiments that lead to insights for the research topic.
```
```
You are a harsh and critical but fair reviewer who is looking for an idea that would be impactful in the field.
```
```
You are a harsh but fair open-minded reviewer that is looking for novel ideas that have not been proposed before.
```

Review JSON template (excerpt):
```
Respond in the following format:

THOUGHT:
<THOUGHT>

REVIEW JSON:
```json
<JSON>
```

In <JSON>, provide the review in JSON format with the following fields in the order:
- "Summary", "Strengths", "Weaknesses", "Originality", "Quality", "Clarity", "Significance"
- "Questions", "Limitations", "Ethical Concerns", "Soundness", "Presentation", "Contribution"
- "Overall" (1-10), "Confidence" (1-5), "Decision" (Accept or Reject only)
```

Professor readme prompt:
```
You are {role_description}
Here is the written paper
{report}
Task instructions: Your goal is to integrate all of the knowledge, code, reports, and notes provided to you and generate a readme.md for a github repository.
```

### Minimal code
```python
class ReviewersAgent:
    def inference(self, plan, report):
        reviews = [
            get_score(plan, report, reviewer_type="You are a harsh but fair reviewer..."),
            get_score(plan, report, reviewer_type="You are a harsh and critical but fair reviewer..."),
            get_score(plan, report, reviewer_type="You are a harsh but fair open-minded reviewer..."),
        ]
        return "\n".join(reviews)
```

### Caveats
- **Fragment from AgentLaboratory** — missing imports (`BaseAgent`, `query_model`, `get_score` body incomplete)
- Second cell is **empty**
- Not runnable standalone; reference only from https://github.com/SamuelSchmidgall/AgentLaboratory
- `get_score` has `attempts=3` retry loop but exception handling abbreviated

---

## Failure modes (skill-level)
- Unanchored exploration never converges
- Single reviewer bias
- Notebook fragment not runnable standalone

## Chains with
`reasoning-techniques`, `rag`
