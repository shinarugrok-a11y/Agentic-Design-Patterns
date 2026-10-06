# Routing — deep dive

Source: Chapter 2 (GT:L1204–L1796) + `Chapter_02_Routing_(Google_ADK).ipynb`,
`Chapter_02_Routing_(LangGraph).ipynb`.
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

Filing notes (verified, files left in place):
- `Chapter_02_Routing_(Openrouter).ipynb` is misfiled. Its code is the Ch 16
  "Hands-On Code Example (OpenRouter)" (GT:L9808–L9836); Ch 2 never mentions
  OpenRouter. See `resource-aware-optimization` deep-dive, Pattern C.
- `Chapter_02_Routing_(LangGraph).ipynb` imports LangChain only
  (`RunnableBranch`); it contains no LangGraph code.

## Rule of thumb (SOURCE, GT:L1737–L1742)
Use when an agent must decide between multiple distinct workflows, tools or
sub-agents based on the user's input or current state. Canonical case: a
support bot distinguishing sales, technical support and account questions.

## Routing mechanisms (SOURCE terms, GT:L1237–L1259; trade-off column DERIVED)
| Mechanism | How | Trade-off |
|---|---|---|
| LLM-based | Prompt the model to emit a label | Flexible; needs output normalisation |
| Embedding-based | Similarity of query to route descriptions | Cheap, no generation; needs good descriptions |
| Rule-based | Keywords, regex, structured fields | Deterministic; brittle to phrasing |
| ML model-based | Discriminative model trained on labelled data | Fast; needs data |

## Pattern A: ADK coordinator with LLM-driven delegation (Auto-Flow)
Provenance: SOURCE (abridged) — condensed from GT:L1575–L1617 and `Chapter_02_Routing_(Google_ADK).ipynb`; descriptions shortened, tool wrappers inlined.
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
The coordinator matches requests against the sub-agents' `description`
fields, so write them as disjoint, action-oriented sentences (DERIVED advice).
The book notes that its `unclear_handler` "is included as a fallback" but the
coordinator logic "doesn't explicitly use it" (GT:L1700–L1702): the ADK
example has no working default route.

Run loop (InMemoryRunner):
Provenance: SOURCE (abridged) — condensed from GT:L1620–L1650; the book awaits `create_session` inside an `async def`.
```python
runner = InMemoryRunner(coordinator)
await runner.session_service.create_session(app_name=runner.app_name, user_id=uid, session_id=sid)
for event in runner.run(user_id=uid, session_id=sid,
                        new_message=types.Content(role="user", parts=[types.Part(text=req)])):
    if event.is_final_response() and event.content:
        text = "".join(p.text for p in event.content.parts if p.text)
        break
```

## Pattern B: LangChain router chain + RunnableBranch
Provenance: SOURCE (abridged) — from GT:L1401–L1453 and `Chapter_02_Routing_(LangGraph).ipynb`; dict-literal input reformatted.
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
Notes:
- `.strip()` on the decision is in the book code (GT:L1437–L1440, "Added .strip()").
- The default (`unclear`) branch is the last positional argument of `RunnableBranch`.
- The original request travels alongside the decision via `RunnablePassthrough`.

## Model-level routing is Chapter 16, not Chapter 2
The OpenRouter gateway example (`"model": "openrouter/auto"`, or an ordered
`"models"` list for sequential fallback) is in Ch 16 (GT:L9808–L9876). Use
`resource-aware-optimization` when the routing axis is cost or capability
rather than intent.

## Prompt template for a classifier router
Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```
Classify the request into exactly one of: {labels}.
Definitions:
{label}: {one-line definition}
...
Respond with the label only, lowercase, no punctuation.
Request: {request}
```

## Anti-patterns (DERIVED)
- Coordinator that also answers: it will answer instead of delegating.
- Overlapping route definitions; LLM delegation becomes non-deterministic.
- No fallback route; unknown intents raise or loop.
- Routing on a long, expensive model when a small classifier suffices.

## Pattern variants (DERIVED summary; book terms cited where present)
- **LLM-based routing** (SOURCE, GT:L1237) — a prompt classifies the query and emits one route id.
- **Embedding-based routing** (SOURCE, GT:L1244) — embed the query, compare to per-route embeddings.
- **Rule-based routing** (SOURCE, GT:L1250) — if/else over keywords, patterns or structured fields; fast and deterministic, brittle on unseen inputs.
- **ML model-based routing** (SOURCE, GT:L1254) — a discriminative model trained on labelled data.
- **Agent delegation** (SOURCE, GT:L1613–L1615) — the router is a coordinator agent with `sub_agents`; ADK Auto-Flow performs the handoff.
- **Model-level routing** — see Ch 16 / `resource-aware-optimization`.

## More prompt templates
Provenance: SOURCE — book router prompt (GT:L1401–L1410), line-wrapped.
```text
Analyze the user's request and determine which specialist handler should
process it.
 - If the request is related to booking flights or hotels, output 'booker'.
 - For all other general information questions, output 'info'.
 - If the request is unclear or doesn't fit either category, output 'unclear'.
ONLY output one word: 'booker', 'info', or 'unclear'.
```

Provenance: SOURCE — book coordinator instruction (GT:L1599–L1610), line-wrapped.
```text
You are the main coordinator. Your only task is to analyze incoming user
requests and delegate them to the appropriate specialist agent. Do not try
to answer the user directly.
- For any requests related to booking flights or hotels, delegate to the
  'Booker' agent.
- For all other general information questions, delegate to the 'Info' agent.
```

## Framework notes
- **LangChain** (SOURCE) — `RunnableBranch` for a single dispatch (GT:L1436).
- **LangGraph** — named in the Ch 2 key takeaways (GT:L1758–L1760) without Ch 2 code; conditional-edge code appears in Ch 17 (GT:L10817).
- **Google ADK** (SOURCE) — routing is implicit: each sub-agent's `description` is what the coordinator's LLM matches against.

## Failure modes in depth (DERIVED)
- **Overlapping route descriptions** — two routes match the same query, so selection flips run to run. Write mutually exclusive descriptions with explicit negative cases; the book's LangChain example sets `temperature=0` (GT:L1371).
- **No fallback route** — unmatched input dead-ends or silently picks the last branch. Define an `unclear`/`other` terminal route; the ADK example in the book lacks one (GT:L1700–L1702).
- **Hallucinated route id** — the model emits a label outside the catalog. Constrain output to one word, validate the id against the route dict, fall back on a miss.
- **Misroute derails downstream work** — log the route id and rationale; let handlers reject inputs outside their domain.
