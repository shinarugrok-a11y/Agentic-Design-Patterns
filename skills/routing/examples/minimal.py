"""Routing: classify a request, then dispatch to exactly one handler.

Uses a stub classifier so it runs offline. Replace `classify` with an LLM
call that returns one of the labels (remember to `.strip()` the output).
"""
from typing import Callable, Dict


def booking_handler(request: str) -> str:
    return f"[Booker] simulated booking for: {request!r}"


def info_handler(request: str) -> str:
    return f"[Info] simulated lookup for: {request!r}"


def unclear_handler(request: str) -> str:
    return f"[Coordinator] could not route: {request!r}. Please clarify."


HANDLERS: Dict[str, Callable[[str], str]] = {"booker": booking_handler, "info": info_handler}


def classify(request: str) -> str:
    """Stand-in for: llm('Output one word: booker|info|unclear ...').strip()"""
    words = request.lower()
    if any(k in words for k in ("book", "flight", "hotel")):
        return "booker"
    if words.endswith("?"):
        return "info"
    return "unclear"


def route(request: str) -> str:
    decision = classify(request).strip()
    handler = HANDLERS.get(decision, unclear_handler)  # default branch is mandatory
    return handler(request)


if __name__ == "__main__":
    for req in ["Book me a hotel in Paris.", "What is the highest mountain?", "Tell me a random fact."]:
        print(route(req))
