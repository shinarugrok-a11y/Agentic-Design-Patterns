# Resource-Aware Optimization — Pattern reference

Load this file only when implementing `resource-aware-optimization`. Do not load by default.

## Book (Gulli) — rule of thumb
Use under tight cost/latency/hardware budgets; route cheap models first and degrade gracefully.

## Book — visual (figure captions; images stay in the PDF)
Fig. 2: Resource-Aware Optimization Design Pattern (tier models; OpenRouter as example gateway).

## Notebooks (extracted)

Resource-Aware Optimization

### Notebooks
- `Chapter_16_Resource_Optimization_(Code_Snippets).ipynb` *(conceptual, not runnable)*
- `Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb`

### Patterns
- **Model tiering:** `gemini-2.5-pro` for complex vs `gemini-2.5-flash` for simple
- **Query router:** custom `BaseAgent` routes by query length threshold
- **Classifier → model routing:** classify as `simple` / `reasoning` / `internet_search` → pick model + optional Google CSE
- **Model mapping:** simple→`gpt-4o-mini`, reasoning→`o4-mini`, search→`gpt-4o` with injected context

### Prompt templates
Classifier system message:
```
You are a classifier that analyzes user prompts and returns one of three categories ONLY:

- simple
- reasoning
- internet_search

Rules:
- Use 'simple' for direct factual questions that need no reasoning or current events.
- Use 'reasoning' for logic, math, or multi-step inference questions.
- Use 'internet_search' if the prompt refers to current events, recent data, or things not in your training data.

Respond ONLY with JSON like:
{ "classification": "simple" }
```

Critic agent (conceptual):
```
You are the **Critic Agent**, serving as the quality assurance arm of our collaborative research assistant system...
All criticism must be constructive. Your goal is to fortify the research, not invalidate it.
```

### Minimal code
```python
def handle_prompt(prompt: str) -> dict:
    classification = classify_prompt(prompt)["classification"]
    search_results = google_search(prompt) if classification == "internet_search" else None
    answer, model = generate_response(prompt, classification, search_results)
    return {"classification": classification, "response": answer, "model": model}
```

### Caveats
- Code_Snippets explicitly marked **"Conceptual Python-like structure, not runnable code"**
- OI example needs `OPENAI_API_KEY`, `GOOGLE_CUSTOM_SEARCH_API_KEY`, `GOOGLE_CSE_ID`
- Word-count routing is a toy heuristic — not production-ready
- Classifier uses `temperature=1` — may add variance

---

## Failure modes (skill-level)
- Naive length heuristics mis-route hard short questions
- Classifier temperature too high
- No fallback when the cheap model fails

## Chains with
`routing`, `prioritization`
