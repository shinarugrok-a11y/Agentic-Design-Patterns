# Multi-Agent Collaboration

Ch 7.

## Frameworks
- Google ADK (SequentialAgent, ParallelAgent, LoopAgent, agent_tool, custom coordinator); CrewAI (Agent/Task/Crew).

## Key APIs from the notebooks
- `ADK: SequentialAgent / ParallelAgent / LoopAgent compositions`
- `ADK: agent_tool wraps an LlmAgent as a callable tool; TaskExecutor(BaseAgent)._run_async_impl coordinator`
- `ADK: ConditionChecker(BaseAgent) as loop exit gate`

## Code patterns
- Pattern: define roles -> pick topology -> typed handoffs -> run -> merge.
- Topologies: Sequential (pipeline), Parallel (fan-out), Loop (iterate w/ exit check), Coordinator (dispatcher).
- Custom coordinator extends BaseAgent and implements _run_async_impl.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_07_Multi_Agent_(ADK_Gemini_AgentTool).ipynb`
- `chapter_notebooks/Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator).ipynb`
- `chapter_notebooks/Chapter_07_Multi_Agent_(ADK_Gemini_Loop).ipynb`
- `chapter_notebooks/Chapter_07_Multi_Agent_(ADK_Gemini_Parallel).ipynb`
- `chapter_notebooks/Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb`
- `chapter_notebooks/Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb`

