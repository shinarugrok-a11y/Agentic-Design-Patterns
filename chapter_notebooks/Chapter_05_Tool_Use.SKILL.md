---
name: tool-use
description: Function calling to reach outside the model. Declare external functions and let the model emit a structured call when it needs real-world data or actions. Skip it when the answer is already in context or no side effect is required.
role: [executor]
chapter: 5
token_cost_estimate: 370
chains_with: [model-context-protocol, exception-handling-and-recovery, guardrails-safety]
---

# Tool Use

## When to use
- Task needs real-time, private, or precise data
- An action must take effect in an external system
- Computation or code execution must be exact

## When NOT to use
- The answer is already in context
- The call's cost or risk exceeds its value
- No schema can be defined for the arguments

## Inputs
- tool schemas with descriptions
- user request
- credentials or scopes

## Outputs
- tool call arguments
- tool result
- final grounded answer

## Failure modes
- Vague tool descriptions cause wrong-tool selection
- Hallucinated or malformed arguments fail schema validation
- Unvalidated side effects fire without confirmation
- Tool errors returned raw to the model trigger retry loops

## Minimal example
```python
@tool
def get_weather(city: str) -> str:
    """Return current weather for a city. Use for live conditions only."""
    return api.fetch(city)

agent = create_tool_calling_agent(llm, [get_weather], prompt)
AgentExecutor(agent=agent, tools=[get_weather]).invoke({"input": q})
```

## Next skills
- If tools are remote or shared: load `model-context-protocol`
- If calls can fail: load `exception-handling-and-recovery`
- If a call is irreversible: load `guardrails-safety`
