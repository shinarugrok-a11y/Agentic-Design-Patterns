# Multi-Agent Collaboration — deep dive

Source: Chapter 7 + six notebooks: `Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator)`,
`(ADK_Gemini_Sequential)`, `(ADK_Gemini_Parallel)`, `(ADK_Gemini_Loop)`,
`(ADK_Gemini_AgentTool)`, `(CrewAI_Gemini)`.

## Interaction models (book)
Sequential handoff, parallel workstreams, debate/consensus, hierarchical
delegation, expert teams, critic-reviewer. Rule of thumb: use when a task
decomposes into sub-tasks needing distinct expertise, tools or stages.

## ADK building blocks
| Construct | Behaviour | State handoff |
|---|---|---|
| `LlmAgent(sub_agents=[...])` | Coordinator; LLM-driven delegation | any |
| `SequentialAgent` | Run children in order | `output_key` -> `state['key']` |
| `ParallelAgent` | Run children concurrently, join | each child `output_key` |
| `LoopAgent(max_iterations=n)` | Repeat children until `escalate` | state flag |
| `agent_tool.AgentTool(agent=...)` | Expose an agent as a callable tool | tool result |
| `BaseAgent._run_async_impl` | Custom non-LLM agent | yields `Event`s |

### Coordinator (hierarchical)
```python
class TaskExecutor(BaseAgent):
    name: str = "TaskExecutor"
    description: str = "Executes a predefined task."
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        yield Event(author=self.name, content="Task finished successfully.")

greeter = LlmAgent(name="Greeter", model="gemini-2.0-flash-exp", instruction="You are a friendly greeter.")
coordinator = LlmAgent(name="Coordinator", model="gemini-2.0-flash-exp",
    description="A coordinator that can greet users and execute tasks.",
    instruction="When asked to greet, delegate to the Greeter. When asked to perform a task, delegate to the TaskExecutor.",
    sub_agents=[greeter, TaskExecutor()])
assert greeter.parent_agent == coordinator
```

### Sequential
```python
step1 = Agent(name="Step1_Fetch", output_key="data")
step2 = Agent(name="Step2_Process",
              instruction="Analyze the information found in state['data'] and provide a summary.")
pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])
```

### Parallel
```python
weather_fetcher = Agent(name="weather_fetcher", model="gemini-2.0-flash-exp",
    instruction="Fetch the weather for the given location and return only the weather report.",
    output_key="weather_data")
news_fetcher = Agent(name="news_fetcher", model="gemini-2.0-flash-exp",
    instruction="Fetch the top news story for the given topic and return only that story.",
    output_key="news_data")
data_gatherer = ParallelAgent(name="data_gatherer", sub_agents=[weather_fetcher, news_fetcher])
```

### Loop with condition checker
```python
class ConditionChecker(BaseAgent):
    name: str = "ConditionChecker"
    description: str = "Checks if a process is complete and signals the loop to stop."
    async def _run_async_impl(self, context):
        if context.session.state.get("status", "pending") == "completed":
            yield Event(author=self.name, actions=EventActions(escalate=True))   # stop loop
        else:
            yield Event(author=self.name, content="Condition not met, continuing loop.")

process_step = LlmAgent(name="ProcessingStep", model="gemini-2.0-flash-exp",
    instruction="You are a step in a longer process. Perform your task. If you are the final step, update session state by setting 'status' to 'completed'.")
poller = LoopAgent(name="StatusPoller", max_iterations=10, sub_agents=[process_step, ConditionChecker()])
```

### Agent as tool
```python
image_generator_agent = LlmAgent(name="ImageGen", model="gemini-2.0-flash",
    description="Generates an image based on a detailed text prompt.",
    instruction=("You are an image generation specialist. Take the user's request and use the "
                 "`generate_image` tool to create the image. The user's entire request should be "
                 "used as the 'prompt' argument. After the tool returns the image bytes, output the image."),
    tools=[generate_image])
image_tool = agent_tool.AgentTool(agent=image_generator_agent,
    description="Use this tool to generate an image. The input should be a descriptive prompt of the desired image.")
artist_agent = LlmAgent(name="Artist", model="gemini-2.0-flash",
    instruction="First, invent a creative and descriptive prompt for an image. Then, use the `ImageGen` tool to generate the image using your prompt.",
    tools=[image_tool])
```
`AgentTool` passes the parent's argument as `input` to the child. Keep the
action (the function tool) separate from the reasoning (the child agent).

## CrewAI role/task crew
```python
researcher = Agent(role="Senior Research Analyst",
    goal="Find and summarize the latest trends in AI.",
    backstory="You are an experienced research analyst with a knack for identifying key trends and synthesizing information.",
    allow_delegation=False)
writer = Agent(role="Technical Content Writer",
    goal="Write a clear and engaging blog post based on research findings.",
    backstory="You are a skilled writer who can translate complex technical topics into accessible content.",
    allow_delegation=False)

research_task = Task(description="Research the top 3 emerging trends in Artificial Intelligence in 2024-2025. Focus on practical applications and potential impact.",
    expected_output="A detailed summary of the top 3 AI trends, including key points and sources.", agent=researcher)
writing_task = Task(description="Write a 500-word blog post based on the research findings. The post should be engaging and easy for a general audience to understand.",
    expected_output="A complete 500-word blog post about the latest AI trends.", agent=writer,
    context=[research_task])                      # handoff

Crew(agents=[researcher, writer], tasks=[research_task, writing_task], process=Process.sequential, llm=llm).kickoff()
```

## Design checklist
- Coordinator instruction: "Delegate only. Do not answer directly."
- Sub-agent `description` is the routing signal; keep them disjoint.
- Name state keys once and reference them verbatim in instructions.
- Loops: always set `max_iterations` and a checker that escalates.
- Consider `a2a` when agents live on different frameworks/hosts.

## Pattern variants
- **Sequential handoff** — a fixed pipeline where each agent's output feeds the next; wins for staged work (research → write → edit).
- **Parallel workstream** — independent agents run at once and their results are merged; wins when subtasks share no dependency.
- **Hierarchical delegation** — a coordinator routes each request to the sub-agent holding the right tools; wins when the split is decided at runtime.
- **Agent-as-tool** — a specialist wrapped in `AgentTool` so the caller sees one tool, not a peer; wins for delegation without giving up the turn.
- **Critic-reviewer / debate** — one group produces, a second assesses it, the original revises; wins for code, research writing, and compliance.
- **Bounded loop** — worker plus condition checker, repeating until a state flag flips.

## More prompt templates
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

## Framework notes
- **LangChain / LangGraph** — no orchestration role here; it only supplies the model to CrewAI agents.
- **Google ADK** — `SequentialAgent`, `ParallelAgent`, `LoopAgent`, `sub_agents`, and `AgentTool` cover the topologies; `output_key` writes to `session.state`, and `EventActions(escalate=True)` ends a loop.
- **CrewAI** — roles come from `role` / `goal` / `backstory`; `Task.context` names the upstream tasks whose output is visible downstream.

## Failure modes in depth
- **Coordination overhead exceeds the benefit** — every hop costs a model call. If the subtasks need the same tools, give one agent all of them instead of splitting.
- **Agents duplicate work or deadlock** — give each agent a distinct `output_key` so no two write the same slot, and bound every loop with `max_iterations` plus an explicit escalate condition.
- **Context lost or distorted at handoff** — pass structured state (`state['data']`, `Task.context`) rather than re-summarizing prose at each hop, and instruct the receiver where to read it.
- **Errors compound with no shared critic** — add a critic-reviewer before the final synthesis that judges against stated criteria rather than re-answering the task.
