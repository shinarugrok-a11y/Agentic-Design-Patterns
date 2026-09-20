# Multi-Agent Collaboration — Patterns

## Pattern variants
- **Sequential handoff** — a fixed pipeline where each agent's output feeds the next; wins for staged work (research → write → edit).
- **Parallel workstream** — independent agents run at once and their results are merged; wins when subtasks share no dependency.
- **Hierarchical delegation** — a coordinator routes each request to the sub-agent holding the right tools; wins when the split is decided at runtime.
- **Agent-as-tool** — a specialist wrapped in `AgentTool` so the caller sees one tool, not a peer; wins for delegation without giving up the turn.
- **Critic-reviewer / debate** — one group produces, a second assesses it, the original revises; wins for code, research writing, and compliance.
- **Bounded loop** — worker plus condition checker, repeating until a state flag flips.

## Prompt templates
Coordinator instruction — name the delegate per case, do not describe the work:

```
description: A coordinator that can greet users and execute tasks.
instruction: When asked to greet, delegate to the Greeter. When asked to
             perform a task, delegate to the TaskExecutor.
```

`AgentTool` description — all the parent agent sees of the specialist:

```
Use this tool to generate an image. The input should be a descriptive
prompt of the desired image.
```

## Code patterns
Google ADK (topologies; state is the handoff channel):

```python
step1 = Agent(name="Step1_Fetch", output_key="data")   # -> session.state["data"]
step2 = Agent(name="Step2_Process",
              instruction="Analyze the information found in state['data'] and summarize.")
pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])

gatherer = ParallelAgent(name="data_gatherer", sub_agents=[weather_fetcher, news_fetcher])
poller = LoopAgent(name="StatusPoller", max_iterations=10,
                   sub_agents=[process_step, ConditionChecker()])
```

Google ADK (hierarchy, plus the loop exit signal):

```python
coordinator = LlmAgent(name="Coordinator", model="gemini-2.0-flash-exp",
                       instruction="Delegate greetings to Greeter, tasks to TaskExecutor.",
                       sub_agents=[greeter, task_doer])

class ConditionChecker(BaseAgent):
    async def _run_async_impl(self, context) -> AsyncGenerator[Event, None]:
        if context.session.state.get("status", "pending") == "completed":
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name, content="Condition not met, continuing loop.")
```

CrewAI (explicit context handoff between tasks):

```python
writing_task = Task(description="Write a 500-word blog post from the research findings.",
                    agent=writer, context=[research_task])
crew = Crew(agents=[researcher, writer], tasks=[research_task, writing_task],
            process=Process.sequential)
```

## Framework notes
- **LangChain / LangGraph** — no orchestration role here; it only supplies the model to CrewAI agents.
- **Google ADK** — `SequentialAgent`, `ParallelAgent`, `LoopAgent`, `sub_agents`, and `AgentTool` cover the topologies; `output_key` writes to `session.state`, and `EventActions(escalate=True)` ends a loop.
- **CrewAI** — roles come from `role` / `goal` / `backstory`; `Task.context` names the upstream tasks whose output is visible downstream.

## Failure modes in depth
- **Coordination overhead exceeds the benefit** — every hop costs a model call. If the subtasks need the same tools, give one agent all of them instead of splitting.
- **Agents duplicate work or deadlock** — give each agent a distinct `output_key` so no two write the same slot, and bound every loop with `max_iterations` plus an explicit escalate condition.
- **Context lost or distorted at handoff** — pass structured state (`state['data']`, `Task.context`) rather than re-summarizing prose at each hop, and instruct the receiver where to read it.
- **Errors compound with no shared critic** — add a critic-reviewer before the final synthesis that judges against stated criteria rather than re-answering the task.

## Source
Chapter 7 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_07_Multi_Agent_(ADK_Gemini_X).ipynb for X in Sequential, Parallel, Loop, Coordinator, AgentTool; Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb.
