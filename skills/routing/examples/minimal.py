"""Classify each request into one route id, then dispatch with a mandatory fallback.

Real framework: LangGraph / LCEL RunnableBranch
  {"decision": router_chain, "request": RunnablePassthrough()} | delegation_branch
Run: python3 examples/minimal.py
"""

ROUTER_PROMPT = (
    "Analyze the user's request and output exactly one route id from {routes}.\n"
    "If the request fits none of them, output 'other'.\n\nRequest: {query}"
)


def billing_agent(q: str) -> str:
    return f"Billing handler processed: {q!r}"


def tech_agent(q: str) -> str:
    return f"Tech handler processed: {q!r}"


def human_handoff(q: str) -> str:
    return f"Escalated to a human: {q!r}"


ROUTES = {"billing": billing_agent, "tech": tech_agent, "other": human_handoff}


def llm(prompt: str) -> str:
    """Canned classifier; the last line returns a hallucinated id on purpose."""
    query = prompt.rsplit("Request: ", 1)[1].lower()
    if "invoice" in query or "charge" in query:
        return " billing\n"
    if "crash" in query or "error" in query:
        return "tech"
    return "refunds"  # not in ROUTES — the fallback must absorb it


for query in ["Why was I charged twice on this invoice?",
              "The app crashes on startup",
              "Can you ship me a T-shirt?"]:
    choice = llm(ROUTER_PROMPT.format(query=query, routes=list(ROUTES))).strip()
    # Validate against the catalog: an unknown id falls back, never dispatches.
    route = choice if choice in ROUTES else "other"
    print(f"route={route:8} (model said {choice!r}) -> {ROUTES[route](query)}")
