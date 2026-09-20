# Resource-Aware Optimization — reference patterns

Source: Chapter 16 + `Chapter_16_Resource_Optimization_(Code_Snippets)`,
`Chapter_16_Resource_Optimization_(OI_Google_Search)`.

## Rule of thumb (book)
Use under strict API/compute budgets, in latency-sensitive apps, on
resource-constrained hardware (edge/battery), when programmatically
balancing quality vs. cost, or in multi-step workflows whose steps have
different resource needs.

## Technique catalogue (book)
Dynamic model switching; adaptive tool use & selection; contextual pruning
& summarisation; proactive resource prediction; cost-sensitive exploration
in multi-agent systems; energy-efficient deployment; parallelization /
distributed-computing awareness; learned resource allocation policies;
graceful degradation & fallbacks; prioritisation of critical tasks.
Also "fallback" (cheaper model if the primary is unavailable) and
"budget-aware" behaviour (stop or simplify when spend approaches a cap).

## Pattern A: ADK router between Flash and Pro (conceptual)
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
Observed: "What is the capital of Australia?" -> simple -> gpt-4o-mini.
Note the classifier itself runs on a strong model; for real savings use a
small model or heuristics for the classification step.

## Cost accounting sketch
```python
COST = {"gpt-4o-mini": 0.15, "o4-mini": 1.10, "gpt-4o": 2.50}   # $/1M input tokens (illustrative)
spend += tokens_in * COST[model] / 1e6
if spend > budget * 0.9: downgrade_tier()
```

## Checklist
- Measure before optimising (`evaluation-monitoring`: latency, tokens).
- Keep a quality floor: sample cheap-path answers for critique.
- Prune context (summaries, windowing) before switching models.
- Define degradation order: model tier -> fewer tools -> shorter output -> refuse.
