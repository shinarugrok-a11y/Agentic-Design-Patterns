# Resource-Aware Optimization — Patterns

## Pattern variants
- **Dynamic model switching** — a router agent classifies complexity and picks Gemini Flash vs. Pro (or gpt-4o-mini vs. o4-mini vs. gpt-4o); the core variant.
- **Adaptive tool selection** — route on what the query needs, not only how hard it is: reach for search only when the answer sits outside training data, since each tool carries its own cost.
- **Critique-agent feedback loop** — a separate critic scores answers and its verdicts retune the router; catches simple-to-Pro and complex-to-Flash misroutes.
- **Sequential model fallback** — an ordered model list; on unavailability, rate limit, or content filter the request re-routes to the next. Continuity, not savings.
- **Other levers in the chapter's spectrum** — contextual pruning and summarization (fewer prompt tokens rather than a cheaper model), proactive resource prediction, energy-efficient edge deployment, graceful degradation.

## Prompt templates

Router/classifier (closed label set plus JSON, so the tier map cannot drift):
```
You are a classifier that analyzes user prompts and returns one of three
categories ONLY: simple, reasoning, internet_search.
- 'simple': direct factual questions needing no reasoning or current events.
- 'reasoning': logic, math, or multi-step inference questions.
- 'internet_search': current events or anything outside your training data.
Respond ONLY with JSON like: { "classification": "simple" }
```

Critic agent (the signal that keeps a cheap tier honest):
```
You are the Critic Agent, the quality assurance arm of this system. Review the
answering agent's output for factual correctness, thoroughness, and bias. Name
missing data or inconsistent reasoning, and propose concrete fixes.
```

## Code patterns

OpenAI SDK (map the label to a model; pay for search only when the label asks):
```python
def generate_response(prompt, classification, search_results=None):
    if classification == "simple":
        model, full_prompt = "gpt-4o-mini", prompt
    elif classification == "reasoning":
        model, full_prompt = "o4-mini", prompt
    else:                                    # internet_search
        model = "gpt-4o"
        context = format_results(search_results) or "No search results found."
        full_prompt = f"Use these web results:\n{context}\n\nQuery: {prompt}"
    resp = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": full_prompt}])
    return resp.choices[0].message.content, model      # report the tier spent
```

Google ADK (router as a `BaseAgent` dispatching to per-tier agents):
```python
class QueryRouterAgent(BaseAgent):
    name: str = "QueryRouter"

    async def _run_async_impl(self, context: InvocationContext):
        query_length = len(context.current_message.text.split())
        agent = gemini_flash_agent if query_length < 20 else gemini_pro_agent
        response = await agent.run_async(context.current_message)
        yield Event(author=self.name, content=f"{agent.name} processed: {response}")
```

## Framework notes
- **Google ADK** — tiers are `Agent`s differing only in `model=`; the router is a `BaseAgent` whose `_run_async_impl` yields `Event`s and would `transfer_to_agent` in production.
- **OpenAI SDK / OpenRouter** — OpenRouter does this at the API layer: `"model": "openrouter/auto"`, or an ordered model list for sequential fallback.

## Failure modes in depth
- **Router misjudges complexity** — a word-count heuristic calls a short but hard question simple; back it with a critic agent and let repeated "inadequate Flash answer" verdicts move the threshold.
- **Router overhead exceeds savings** — an LLM classifier on gpt-4o can cost more than the cheap answer it buys; classify with a small model or heuristic, and skip routing where the tier is already known.
- **Budget tracked per call, never in aggregate** — charge a running counter after every call instead of only checking a per-request cap; the router must read remaining budget and time, not just the query.
- **Silent quality degradation** — the caller cannot tell a Flash answer from a Pro one; return the model used with the answer, and mark degraded or fallback results explicitly.

## Source
Chapter 16 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_16_Resource_Optimization_(Code_Snippets).ipynb, Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb.
