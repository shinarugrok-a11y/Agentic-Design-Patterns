# Routing — reference patterns

Source: Chapter 2 + `Chapter_02_Routing_(Google_ADK).ipynb`,
`Chapter_02_Routing_(LangGraph).ipynb`, `Chapter_02_Routing_(Openrouter).ipynb`.

## Rule of thumb (book)
Use when an agent must decide between multiple distinct workflows, tools or
sub-agents based on input or state. Canonical case: support bot triaging
sales vs. technical vs. account questions.

## Routing mechanisms
| Mechanism | How | Trade-off |
|---|---|---|
| LLM-based | Prompt the model to emit a label | Flexible; needs output normalisation |
| Embedding-based | Cosine similarity of query to route descriptions | Cheap, no generation; needs good descriptions |
| Rule-based | Keywords, regex, structured fields | Deterministic; brittle to phrasing |
| ML classifier | Trained on labelled requests | Fast; needs data |

## Pattern A: ADK coordinator with LLM-driven delegation (Auto-Flow)
```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

booking_agent = Agent(name="Booker", model="gemini-2.0-flash",
    description="Handles all flight and hotel booking requests by calling the booking tool.",
    tools=[FunctionTool(booking_handler)])
info_agent = Agent(name="Info", model="gemini-2.0-flash",
    description="Provides general information and answers user questions by calling the info tool.",
    tools=[FunctionTool(info_handler)])

coordinator = Agent(name="Coordinator", model="gemini-2.0-flash",
    instruction=("You are the main coordinator. Your only task is to analyze incoming user "
                 "requests and delegate them to the appropriate specialist agent. Do not try "
                 "to answer the user directly.\n"
                 "- For any requests related to booking flights or hotels, delegate to 'Booker'.\n"
                 "- For all other general information questions, delegate to 'Info'."),
    sub_agents=[booking_agent, info_agent])   # presence of sub_agents enables Auto-Flow
```
The routing decision is made from the sub-agents' `description` fields, so
write them as disjoint, action-oriented sentences.

Run loop (InMemoryRunner):
```python
runner = InMemoryRunner(coordinator)
runner.session_service.create_session(app_name=runner.app_name, user_id=uid, session_id=sid)
for event in runner.run(user_id=uid, session_id=sid,
                        new_message=types.Content(role="user", parts=[types.Part(text=req)])):
    if event.is_final_response() and event.content:
        text = "".join(p.text for p in event.content.parts if p.text)
        break
```

## Pattern B: LangChain router chain + RunnableBranch
```python
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the user's request and determine which specialist handler should process it.
     - If the request is related to booking flights or hotels, output 'booker'.
     - For all other general information questions, output 'info'.
     - If the request is unclear or doesn't fit either category, output 'unclear'.
     ONLY output one word: 'booker', 'info', or 'unclear'."""),
    ("user", "{request}")])
router = coordinator_router_prompt | llm | StrOutputParser()

delegation_branch = RunnableBranch(
    (lambda x: x["decision"].strip() == "booker", branches["booker"]),
    (lambda x: x["decision"].strip() == "info", branches["info"]),
    branches["unclear"])                          # default branch

coordinator_agent = ({"decision": router, "request": RunnablePassthrough()}
                     | delegation_branch | (lambda x: x["output"]))
```
Notes from the notebook:
- `.strip()` on the decision is required; models emit trailing whitespace/newlines.
- Always supply a default (`unclear`) branch.
- Pass the original request alongside the decision with `RunnablePassthrough`.

## Pattern C: model routing via a gateway (OpenRouter)
```python
requests.post("https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": "Bearer <OPENROUTER_API_KEY>"},
    data=json.dumps({"model": "openai/gpt-4o", "messages": [{"role": "user", "content": q}]}))
```
Routing here is at the *model* layer (choose a provider/model per request);
combine with `resource-aware-optimization` for cost-based selection.

## Prompt template for a classifier router
```
Classify the request into exactly one of: {labels}.
Definitions:
{label}: {one-line definition}
...
Respond with the label only, lowercase, no punctuation.
Request: {request}
```

## Anti-patterns
- Coordinator that also answers: it will answer instead of delegating.
- Overlapping route definitions; LLM delegation becomes non-deterministic.
- No fallback route; unknown intents raise or loop.
- Routing on a long, expensive model when a small classifier suffices.
