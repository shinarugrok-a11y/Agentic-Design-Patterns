---
name: memory-management
description: Short-term session state plus long-term searchable memory. Use when the agent must remember. Do NOT use for stateless one-shots.
role: [memory]
chapter: 8
token_cost_estimate: 233
chains_with: [rag, learning-and-adaptation]
---

# Memory Management

## When to use
- Multi-turn chat must keep history
- Track progress or `user:` / `temp:` namespaced state
- Recall preferences across sessions (MemoryService / vector store)

## When NOT to use
- Stateless single question
- Need grounded docs, not chat memory (load `rag`)
- Need the agent to rewrite its own policy from traces (load `learning-and-adaptation`)

## Inputs
- Session service (in-memory, DB, Vertex)
- State keys / `output_key`
- Optional long-term MemoryService

## Outputs
- Mutated `session.state`
- Retrieved memory hits

## Failure modes
- Process restart wipes InMemory*
- Dumping full history blows the window
- Inspecting state mid-event stream

## Minimal example
```python
agent = LlmAgent(instruction="Greet.", output_key="last_greeting")
# after runner.run(...): session.state["last_greeting"]
```

## Next skills
- If memory is a document corpus: load `rag`
- If memory should change future behavior: load `learning-and-adaptation`
