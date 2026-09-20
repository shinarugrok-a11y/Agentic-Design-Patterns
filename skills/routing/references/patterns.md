# Routing — Patterns

## Pattern variants
- **LLM-based routing** — a prompt classifies the query and emits one route id; wins on nuanced or novel phrasing.
- **Embedding-based routing** — embed the query, compare to per-route embeddings, take the most similar; wins for semantic routing where meaning beats keywords.
- **Rule-based routing** — if/else or switch over keywords, patterns, or structured fields; faster and deterministic, but brittle on unseen inputs.
- **ML classifier routing** — a discriminative model fine-tuned on labelled traffic; wins at high volume with stable, well-labelled categories.
- **Agent delegation** — the router is a coordinator agent with `sub_agents`, and the framework's Auto-Flow performs the handoff; wins when each route is itself an agent with its own tools.
- **Model-level routing** — route across models rather than handlers (the chapter's OpenRouter example); wins when the axis is cost or capability, not intent.

## Prompt templates

```text
Analyze the user's request and determine which specialist handler should
process it.
 - If the request is related to booking flights or hotels, output 'booker'.
 - For all other general information questions, output 'info'.
 - If the request is unclear or doesn't fit either category, output 'unclear'.
ONLY output one word: 'booker', 'info', or 'unclear'.
```

```text
You are the main coordinator. Your only task is to analyze incoming user
requests and delegate them to the appropriate specialist agent. Do not try
to answer the user directly.
- For any requests related to booking flights or hotels, delegate to the
  'Booker' agent.
- For all other general information questions, delegate to the 'Info' agent.
```

## Code patterns

LangChain / LangGraph (`RunnableBranch`):

```python
coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

delegation_branch = RunnableBranch(
    (lambda x: x["decision"].strip() == "booker", branches["booker"]),
    (lambda x: x["decision"].strip() == "info", branches["info"]),
    branches["unclear"],          # default branch — always present
)

coordinator_agent = (
    {"decision": coordinator_router_chain, "request": RunnablePassthrough()}
    | delegation_branch
    | (lambda x: x["output"])
)
```

Google ADK (LLM-driven delegation):

```python
coordinator = Agent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="...delegate to 'Booker' or 'Info'...",
    # Declaring sub_agents enables Auto-Flow delegation by default.
    sub_agents=[booking_agent, info_agent],
)
```

## Framework notes
- **LangChain / LangGraph** — `RunnableBranch` for a single dispatch; LangGraph conditional edges when routes rejoin or loop.
- **Google ADK** — routing is implicit: each sub-agent's `description` is what the coordinator's LLM matches against, so descriptions are the route catalog.
- **CrewAI / other** — OpenRouter is shown as a gateway that routes a single `/chat/completions` call to a chosen `model`.

## Failure modes in depth
- **Overlapping route descriptions** — two routes match the same query, so selection flips run to run. Write mutually exclusive descriptions with explicit negative cases, and set `temperature=0`.
- **No fallback route** — unmatched input dead-ends or silently picks the last branch. Always define an `unclear`/`other` terminal route, as `RunnableBranch`'s default argument forces you to.
- **Hallucinated route id** — the model emits a label outside the catalog. Constrain output to one word, then validate the id against the route dict and fall back on a miss rather than dispatching on it.
- **Misroute derails downstream work** — the wrong specialist runs a full workflow before anyone notices. Log the route id and rationale, and let handlers reject inputs that do not match their domain.

## Source
Chapter 2 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_02_Routing_(Google_ADK).ipynb, Chapter_02_Routing_(LangGraph).ipynb, Chapter_02_Routing_(Openrouter).ipynb.
