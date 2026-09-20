# Multi-Agent Collaboration — patterns (Ch 7)

## Pattern
1. Define roles with narrow instructions and tools.
2. Pick a coordination model: sequential, parallel, loop, or coordinator/dispatcher.
3. Share results via named state keys.
4. Add a stop condition for loops.

## Prompt template
```
Coordinator: Route requests to sub-agents. Never answer yourself.
Sub-agent description: Handles flight and hotel bookings only.
Merger: Combine {r1} and {r2} into one report; add no new facts.
```

## Key APIs
- ADK: `LlmAgent(output_key=...)`, `SequentialAgent`, `ParallelAgent`, `LoopAgent(max_iterations=)`, `AgentTool(agent)`.
- CrewAI: `Agent(role, goal, backstory)`, `Task(agent, context)`, `Crew(process=Process.sequential)`.
- Hierarchical: coordinator `sub_agents=[...]` delegates on descriptions.

## Pitfalls -> fixes
- Coordinator answers itself -> instruction 'never answer directly'.
- Key mismatch -> one constant per key, referenced in instructions.
- Endless hand-offs -> `LoopAgent(max_iterations)` or explicit exit tool.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_07_*`.
