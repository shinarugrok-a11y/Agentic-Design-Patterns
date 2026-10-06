# Inter-Agent Communication — patterns (Ch 15)

## Pattern
1. Server publishes an Agent Card at `/.well-known/agent.json`.
2. Client fetches the card and picks a skill.
3. Client sends JSON-RPC `sendTask` (or `sendTaskSubscribe` to stream).
4. Track task id and status; collect artifacts.

## Prompt template
```
Agent Card skill description: Returns weather for a city.
Client task: What is the weather in Paris? Respond in one sentence.
```

## Key APIs
- Card: `AgentCard(name, url, skills=[AgentSkill(id, description)], capabilities=...)`.
- Server (book): `A2AStarletteApplication(agent_card, http_handler=DefaultRequestHandler(...))`.
- Client (book): `{'jsonrpc': '2.0', 'method': 'sendTask', 'params': {...}}`; newer spec names UNVERIFIED.

## Pitfalls -> fixes
- Card overstates skills -> keep descriptions literal.
- Long tasks time out -> streaming or push notifications.
- Open endpoint -> declare card `authentication.schemes`; enforce it.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_15_*`.
