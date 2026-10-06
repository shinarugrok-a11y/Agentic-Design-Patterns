# Resource-Aware Optimization — deep dive

Source: Chapter 16 (GT:L9386–L10037) + `Chapter_16_Resource_Optimization_(Code_Snippets)`,
`Chapter_16_Resource_Optimization_(OI_Google_Search)`, and the misfiled
`Chapter_02_Routing_(Openrouter).ipynb` (its code is this chapter's OpenRouter example).
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

## Rule of thumb (SOURCE, GT:L9969)
Use under strict API/compute budgets, in latency-sensitive apps, on
resource-constrained hardware (edge/battery), when programmatically
balancing quality vs. cost, or in multi-step workflows whose steps have
different resource needs.

## Technique catalogue (SOURCE, GT:L9891–L9945)
Dynamic model switching; adaptive tool use & selection; contextual pruning
& summarisation; proactive resource prediction; cost-sensitive exploration
in multi-agent systems; energy-efficient deployment; parallelization /
distributed-computing awareness; learned resource allocation policies;
graceful degradation & fallbacks; prioritisation of critical tasks.
Also "fallback" (cheaper model if the primary is unavailable) and
"budget-aware" behaviour (stop or simplify when spend approaches a cap).

## Pattern A: ADK router between Flash and Pro (conceptual)
Provenance: SOURCE (abridged) — condensed from GT:L9472–L9550 (`Chapter_16_Resource_Optimization_(Code_Snippets)`); the book marks it conceptual, not runnable.
```python
gemini_pro_agent = Agent(name="GeminiProAgent", model="gemini-2.5-pro",
    description="A highly capable agent for complex queries.",
    instruction="You are an expert assistant for complex problem-solving.")
gemini_flash_agent = Agent(name="GeminiFlashAgent", model="gemini-2.5-flash",
    description="A fast and efficient agent for simple queries.",
    instruction="You are a quick assistant for straightforward questions.")

class QueryRouterAgent(BaseAgent):
    name: str = "QueryRouter"
    description: str = "Routes user queries to the appropriate LLM agent based on complexity."
    async def _run_async_impl(self, context):
        user_query = context.current_message.text
        query_length = len(user_query.split())          # crude proxy for complexity
        if query_length < 20:
            response = await gemini_flash_agent.run_async(context.current_message)
            yield Event(author=self.name, content=f"Flash Agent processed: {response}")
        else:
            response = await gemini_pro_agent.run_async(context.current_message)
            yield Event(author=self.name, content=f"Pro Agent processed: {response}")
```
Add a **Critique Agent** that scores responses and feeds back into routing:
Provenance: SOURCE (abridged) — Critic Agent prompt condensed from GT:L9573–L9590.
```
You are the **Critic Agent**, serving as the quality assurance arm of our collaborative research
assistant system. Your primary function is to **meticulously review and challenge** information from
the Researcher Agent, guaranteeing **accuracy, completeness, and unbiased presentation**.
Your duties encompass: assessing research findings for factual correctness, thoroughness, and potential
leanings; identifying any missing data or inconsistencies in reasoning; raising critical questions;
offering constructive suggestions; validating that the final output is comprehensive and balanced.
All criticism must be constructive. Structure your feedback clearly, drawing attention to specific points for revision.
```

## Pattern B: classifier -> model tier (+ optional search)
Provenance: SOURCE (abridged) — condensed from GT:L9654–L9773 (`Chapter_16_Resource_Optimization_(OI_Google_Search)`); error handling and prints removed.
```python
def classify_prompt(prompt: str) -> dict:
    system_message = {"role": "system", "content": (
        "You are a classifier that analyzes user prompts and returns one of three categories ONLY:\n\n"
        "- simple\n- reasoning\n- internet_search\n\n"
        "Rules:\n"
        "- Use 'simple' for direct factual questions that need no reasoning or current events.\n"
        "- Use 'reasoning' for logic, math, or multi-step inference questions.\n"
        "- Use 'internet_search' if the prompt refers to current events, recent data, or things not in your training data.\n\n"
        'Respond ONLY with JSON like:\n{ "classification": "simple" }')}
    reply = client.chat.completions.create(model="gpt-4o",
        messages=[system_message, {"role": "user", "content": prompt}]).choices[0].message.content
    return json.loads(reply)

def google_search(query, num_results=1):
    r = requests.get("https://www.googleapis.com/customsearch/v1",
                     params={"key": KEY, "cx": CSE_ID, "q": query, "num": num_results})
    return [{"title": i["title"], "snippet": i["snippet"], "link": i["link"]} for i in r.json().get("items", [])]

def generate_response(prompt, classification, search_results=None):
    if classification == "simple":      model, full_prompt = "gpt-4o-mini", prompt
    elif classification == "reasoning": model, full_prompt = "o4-mini", prompt
    else:
        model = "gpt-4o"
        ctx = "\n".join(f"Title: {i['title']}\nSnippet: {i['snippet']}\nLink: {i['link']}" for i in search_results or []) or "No search results found."
        full_prompt = f"Use the following web results to answer the user query:\n\n{ctx}\n\nQuery: {prompt}"
    return client.chat.completions.create(model=model, messages=[{"role": "user", "content": full_prompt}]).choices[0].message.content, model

def handle_prompt(prompt):
    cls = classify_prompt(prompt)["classification"]
    results = google_search(prompt) if cls == "internet_search" else None
    answer, model = generate_response(prompt, cls, results)
    return {"classification": cls, "response": answer, "model": model}
```
The notebook's sample prompt "What is the capital of Australia?" is meant to
classify as simple -> gpt-4o-mini; this was not executed here (needs API keys).
Model ids are time-specific (UNCERTAIN today). DERIVED note: the classifier itself runs on a strong model; for real savings use a
small model or heuristics for the classification step.

## Pattern C: model routing through a gateway (OpenRouter)
Provenance: SOURCE — verbatim, GT:L9814–L9834; identical to notebook cell 0 of the misfiled `Chapter_02_Routing_(Openrouter).ipynb`.
```python
import requests
import json
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer <OPENROUTER_API_KEY>",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "openai/gpt-4o", # Optional
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)
```
`<OPENROUTER_API_KEY>` is a placeholder: read the key from an environment
variable in real code, never inline it.

The book names two OpenRouter routing modes (SOURCE, GT:L9846–L9876):
automated selection with `"model": "openrouter/auto"`, and sequential model
fallback with an ordered `"models": [...]` list where the next model is tried
on unavailability, rate limiting or content filtering. Current OpenRouter
behaviour was not checked (UNCERTAIN).

## Cost accounting sketch
Provenance: DERIVED — ILLUSTRATIVE, not from the book. The book gives no prices; fill `PRICE_PER_1M` from your provider's current price list.
```python
spend += tokens_in * PRICE_PER_1M[model] / 1e6
if spend > budget * 0.9:
    model = next_cheaper_tier(model)
```

## Checklist (DERIVED)
- Measure before optimising (`evaluation-monitoring`: latency, tokens).
- Keep a quality floor: sample cheap-path answers for critique.
- Prune context (summaries, windowing) before switching models.
- Define degradation order: model tier -> fewer tools -> shorter output -> refuse.

## Pattern variants (SOURCE terms, GT:L9891–L9945; glosses DERIVED)
- **Dynamic model switching** — a router agent classifies complexity and picks Gemini Flash vs. Pro (or gpt-4o-mini vs. o4-mini vs. gpt-4o); the core variant.
- **Adaptive tool selection** — route on what the query needs, not only how hard it is: reach for search only when the answer sits outside training data, since each tool carries its own cost.
- **Critique-agent feedback loop** — a separate critic scores answers and its verdicts retune the router; catches simple-to-Pro and complex-to-Flash misroutes.
- **Sequential model fallback** — an ordered model list; on unavailability, rate limit, or content filter the request re-routes to the next. Continuity, not savings.
- **Other levers in the chapter's spectrum** — contextual pruning and summarization (fewer prompt tokens rather than a cheaper model), proactive resource prediction, energy-efficient edge deployment, graceful degradation.

## More prompt templates
Router/classifier (closed label set plus JSON, so the tier map cannot drift):
Provenance: SOURCE (abridged) — reworded from the `classify_prompt` system message, GT:L9655–L9672.
```
You are a classifier that analyzes user prompts and returns one of three
categories ONLY: simple, reasoning, internet_search.
- 'simple': direct factual questions needing no reasoning or current events.
- 'reasoning': logic, math, or multi-step inference questions.
- 'internet_search': current events or anything outside your training data.
Respond ONLY with JSON like: { "classification": "simple" }
```

Critic agent (the signal that keeps a cheap tier honest):
Provenance: SOURCE (abridged) — shortened from GT:L9573–L9590.
```
You are the Critic Agent, the quality assurance arm of this system. Review the
answering agent's output for factual correctness, thoroughness, and bias. Name
missing data or inconsistent reasoning, and propose concrete fixes.
```

## Framework notes
- **Google ADK** (SOURCE) — tiers are `Agent`s differing only in `model=`; the router is a `BaseAgent` whose `_run_async_impl` yields `Event`s; the book comments that a real setup would use `transfer_to_agent` (GT:L9533).
- **OpenAI SDK** (SOURCE) — Pattern B.
- **OpenRouter** (SOURCE) — Pattern C: routing at the API layer.

## Failure modes in depth (DERIVED)
- **Router misjudges complexity** — a word-count heuristic calls a short but hard question simple; back it with a critic agent and let repeated "inadequate Flash answer" verdicts move the threshold.
- **Router overhead exceeds savings** — an LLM classifier on gpt-4o can cost more than the cheap answer it buys; classify with a small model or heuristic, and skip routing where the tier is already known.
- **Budget tracked per call, never in aggregate** — charge a running counter after every call instead of only checking a per-request cap; the router must read remaining budget and time, not just the query.
- **Silent quality degradation** — the caller cannot tell a Flash answer from a Pro one; return the model used with the answer, and mark degraded or fallback results explicitly.
