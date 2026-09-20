# Inter-Agent Communication — patterns (Ch 15)

## Pattern
1. Server publishes an Agent Card at `/.well-known/agent.json`.
2. Client fetches the card and picks a skill.
3. Client sends JSON-RPC `message/send` (or stream).
4. Track task id and status; collect artifacts.

## Prompt template
```
Agent Card skill description: Returns weather for a city.
Client task: What is the weather in Paris? Respond in one sentence.
```

## Key APIs
- Card: `AgentCard(name, url, skills=[AgentSkill(id, description)], capabilities=...)`.
- ADK: `to_a2a(root_agent, port=8001)` exposes an agent; `RemoteA2aAgent` consumes one.
- Client: `requests.post(url, json={'jsonrpc': '2.0', 'method': 'message/send', ...})`.

## Pitfalls -> fixes
- Card overstates skills -> keep descriptions literal.
- Long tasks time out -> streaming or push notifications.
- Open endpoint -> auth in card `securitySchemes`.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_15_*`.
