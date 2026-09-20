"""Tool use: model emits a structured call, runtime executes it, result returns.

Offline stub of the function-calling loop. In production `decide` is the
model with tool schemas bound; everything else is identical.
"""
import inspect
import json
from typing import Callable, Dict


def get_stock_price(ticker: str) -> float:
    """Return the latest simulated price for a ticker. Raises ValueError if unknown."""
    prices = {"AAPL": 178.15, "GOOGL": 1750.30, "MSFT": 425.50}
    if ticker.upper() not in prices:
        raise ValueError(f"ticker '{ticker}' not found")
    return prices[ticker.upper()]


TOOLS: Dict[str, Callable] = {"get_stock_price": get_stock_price}


def tool_schemas() -> list[dict]:
    """What the model sees: name, description (docstring) and parameters."""
    return [{"name": n, "description": inspect.getdoc(f),
             "parameters": list(inspect.signature(f).parameters)} for n, f in TOOLS.items()]


def decide(user_input: str) -> dict | None:
    """Stand-in for the LLM choosing a tool. Returns a structured call or None."""
    for word in user_input.replace("?", "").split():
        if word.isupper() and word.isalpha():
            return {"name": "get_stock_price", "args": {"ticker": word}}
    return None


def run(user_input: str) -> str:
    call = decide(user_input)
    if call is None:
        return "No tool needed; answering from model knowledge."
    try:
        result = TOOLS[call["name"]](**call["args"])
        observation = {"status": "success", "result": result}
    except ValueError as e:                     # expected failure -> structured, not swallowed
        observation = {"status": "error", "error_message": str(e)}
    # The observation is fed back to the model for the final answer.
    return f"call={json.dumps(call)} -> observation={json.dumps(observation)}"


if __name__ == "__main__":
    print(json.dumps(tool_schemas(), indent=2))
    print(run("What is the price of AAPL?"))
    print(run("What is the price of ZZZZ?"))
