# Reflection — Pattern reference

Load this file only when implementing `reflection`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when output quality needs a generate→critique→revise loop against a rubric or goal.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Reflection design pattern, self-reflection. Fig. 2: Producer and critique agent.

## Notebooks (extracted)

Reflection

### Notebooks
- `Chapter_04_Reflection_(ADK).ipynb`
- `Chapter_04_Reflection_(Iterative_Loop).ipynb`
- `Chapter_04_Reflection_(LangChain).ipynb`

### Patterns
- **ADK:** `SequentialAgent` — generator writes to `output_key="draft_text"`, reviewer reads state and outputs structured dict to `review_output`
- **Iterative loop:** generate → reflect → refine until `CODE_IS_PERFECT` or max iterations
- **LangChain:** LCEL pipeline: generate → critique → refine via `RunnablePassthrough.assign`

### Prompt templates
Fact-checker (ADK):
```
You are a meticulous fact-checker.
1. Read the text provided in the state key 'draft_text'.
2. Carefully verify the factual accuracy of all claims.
3. Your final output must be a dictionary containing two keys:
   - "status": A string, either "ACCURATE" or "INACCURATE".
   - "reasoning": A string providing a clear explanation for your status, citing specific issues if any are found.
```

Reflector (Iterative Loop):
```
You are a senior software engineer and an expert in Python.
Your role is to perform a meticulous code review.
Critically evaluate the provided Python code based on the original task requirements.
Look for bugs, style issues, missing edge cases, and areas for improvement.
If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
Otherwise, provide a bulleted list of your critiques.
```

### Minimal code
```python
# ADK write-and-review pipeline
from google.adk.agents import SequentialAgent, LlmAgent

generator = LlmAgent(name="DraftWriter", instruction="Write a short paragraph.", output_key="draft_text")
reviewer = LlmAgent(name="FactChecker", instruction="Review state['draft_text']...", output_key="review_output")
pipeline = SequentialAgent(name="WriteAndReview_Pipeline", sub_agents=[generator, reviewer])
```

```python
# LangChain single-pass reflection
full_reflection_chain = (
    RunnablePassthrough.assign(initial_description=generation_chain)
    | RunnablePassthrough.assign(critique=critique_chain)
    | refinement_chain
)
```

### Caveats
- Iterative loop requires `OPENAI_API_KEY`; uses `gpt-4o` at low temperature
- LangChain reflection is single-pass (not looped) unlike iterative example
- ADK reviewer expects structured dict output — validate parsing in production

---

## Failure modes (skill-level)
- Critic always complains → infinite refine
- Self-review without a stop phrase never exits
- Critic and generator share one prompt and go easy

## Chains with
`prompt-chaining`, `evaluation-monitoring`
