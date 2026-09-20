# Multi-Agent Collaboration — Pattern reference

Load this file only when implementing `multi-agent`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when one agent lacks the skills/tools and the work splits into specialized roles (handoff, parallel, hierarchy).

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Example multi-agent system. Fig. 2: Agents communicate in various ways. Fig. 3: Multi-Agent design pattern.

## Notebooks (extracted)

Multi-Agent Collaboration

### Notebooks
- `Chapter_07_Multi_Agent_(ADK_Gemini_AgentTool).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Loop).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Parallel).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb`
- `Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb`

### Patterns
- **SequentialAgent:** ordered sub-agents; `output_key` passes state between steps
- **ParallelAgent:** concurrent sub-agents writing to distinct state keys
- **LoopAgent:** `max_iterations` + custom `BaseAgent` that `EventActions(escalate=True)` to break
- **AgentTool:** wrap `LlmAgent` as tool; parent calls via `input` parameter
- **Custom BaseAgent:** extend `_run_async_impl` → `AsyncGenerator[Event]`
- **CrewAI:** researcher → writer with `context=[research_task]`; `Process.sequential`

### Prompt templates
ImageGen specialist:
```
You are an image generation specialist. Your task is to take the user's request
and use the `generate_image` tool to create the image.
The user's entire request should be used as the 'prompt' argument for the tool.
After the tool returns the image bytes, you MUST output the image.
```

Coordinator delegation:
```
When asked to greet, delegate to the Greeter. When asked to perform a task, delegate to the TaskExecutor.
```

### Minimal code
```python
# Sequential pipeline
step1 = Agent(name="Step1_Fetch", output_key="data")
step2 = Agent(name="Step2_Process", instruction="Analyze state['data']...")
pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])
```

```python
# Agent-as-tool
image_tool = agent_tool.AgentTool(agent=image_generator_agent, description="Generate an image from a prompt.")
artist = LlmAgent(name="Artist", tools=[image_tool], instruction="Invent a prompt, then call ImageGen.")
```

```python
# CrewAI multi-agent
writing_task = Task(description="Write 500-word blog...", agent=writer, context=[research_task])
Crew(agents=[researcher, writer], tasks=[research_task, writing_task], process=Process.sequential, llm=llm).kickoff()
```

### Caveats
- `Sequential` notebook is minimal (~699 chars) — omits model/instruction on step1
- Loop agent: `ConditionChecker` must read `context.session.state`
- Parallel example has commented-out Runner invocation
- CrewAI requires `GOOGLE_API_KEY` for Gemini

---

## Failure modes (skill-level)
- Coordinator answers instead of delegating
- Loop agent never escalates
- Shared keys collide in parallel runs

## Chains with
`a2a`, `routing`
