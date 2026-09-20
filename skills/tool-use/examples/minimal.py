"""Tool Use: the model emits a structured tool call, the runtime executes it, the result grounds the answer.

Real framework: LangChain @tool + create_tool_calling_agent + AgentExecutor.invoke({"input": q})
Run: python3 examples/minimal.py
"""
import json

TOOLS = {}


def tool(fn):
    """Register a function as a declared tool, like @tool in LangChain or CrewAI."""
    TOOLS[fn.__name__] = fn
    return fn


@tool
def get_weather(city: str) -> str:
    """Return current weather for a city. Use for live conditions only."""
    return {"london": "cloudy, 15C", "paris": "sunny, 22C"}.get(city.lower(), "unknown")


def llm(question: str, scratchpad: list) -> str:
    """Fake model: requests a tool, then answers once a tool result is on the scratchpad."""
    if scratchpad:
        return json.dumps({"final": f"It is currently {scratchpad[-1]} in London."})
    if "weather" in question.lower():
        return json.dumps({"tool": "get_weather", "args": {"city": "London"}})
    return json.dumps({"final": "I can answer that from context alone."})


def agent_executor(question: str, max_steps: int = 3) -> str:
    scratchpad = []
    for step in range(max_steps):
        decision = json.loads(llm(question, scratchpad))
        if "final" in decision:
            return decision["final"]
        name, args = decision["tool"], decision["args"]
        print(f"step {step}: model requested {name}({args})")
        result = TOOLS[name](**args)  # the runtime calls the API, not the model
        print(f"step {step}: tool returned {result!r}")
        scratchpad.append(result)
    return "stopped: step budget exhausted"


question = "What's the weather in London?"
print(f"Q: {question}")
print(f"A: {agent_executor(question)}")
