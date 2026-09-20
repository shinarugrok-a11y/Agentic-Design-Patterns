# Evaluation and Monitoring — patterns (Ch 19)

## Pattern
1. Define metrics: accuracy, latency, tokens, trajectory.
2. Build test cases with expected outputs or rubrics.
3. Use an LLM judge for open-ended outputs.
4. Monitor production traces for drift.

## Prompt template
```
You are an impartial judge. Score the answer 1-5 for accuracy and completeness
against the reference. Return JSON with scores and a one-line reason.
Question: {q}
Reference: {ref}
Answer: {ans}
```

## Key APIs
- ADK: `adk eval` with `.evalset.json`; trajectory (tool call) matching.
- LLM-as-judge: rubric prompt + JSON scores; calibrate on human labels.
- Monitoring: log tokens, latency, tool errors per request.

## Pitfalls -> fixes
- Exact-match on paraphrase -> semantic or judge scoring.
- Judge without rubric -> explicit criteria and scale.
- No cost metrics -> log tokens and latency.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_19_*`.
