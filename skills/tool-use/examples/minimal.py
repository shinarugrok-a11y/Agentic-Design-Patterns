"""Tool Use — minimal runnable demo (stdlib only)."""
import json

def get_stock_price(ticker): return {"ACME": 142.5}.get(ticker.upper(), 0.0)
TOOLS = {"get_stock_price": get_stock_price}

def agent(q):
    if "price" in q.lower():
        ticker = q.split()[-1].strip("?")
        obs = TOOLS["get_stock_price"](ticker)
        return f"{ticker} is ${obs} (via get_stock_price)."
    return "No tool matched."

print(agent("What is the price of ACME?"))
