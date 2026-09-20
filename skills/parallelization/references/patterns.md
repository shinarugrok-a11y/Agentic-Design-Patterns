# Parallelization patterns (Ch 3)

Two notebook variants: Google ADK researcher sub-agents, LangChain `RunnableParallel`.

Pattern A — ADK parallel researchers: define N `LlmAgent` researchers (e.g. RenewableEnergyResearcher with Google Search tool), run them concurrently, then a synthesizer agent merges. Each researcher has a narrow instruction + its own tool.

Pattern B — LangChain RunnableParallel over per-topic chains, optionally with asyncio + RunnablePassthrough. Merge with a final synthesis chain.

Rules: cap fan-out (3-8 branches), set per-branch timeouts, keep the merge prompt explicit about conflict resolution (newest vs most-cited wins).

## Notebook extracts (on-demand detail)

### Chapter_03_Parallelization_(Google_ADK).ipynb

```python
researcher_agent_1 = LlmAgent(
instruction="""You are an AI Research Assistant specializing in energy.
output_key="renewable_energy_result"
researcher_agent_2 = LlmAgent(
instruction="""You are an AI Research Assistant specializing in transportation.
output_key="ev_technology_result"
researcher_agent_3 = LlmAgent(
instruction="""You are an AI Research Assistant specializing in climate solutions.
output_key="carbon_capture_result"
# --- 2. Create the ParallelAgent (Runs researchers concurrently) ---
```

### Chapter_03_Parallelization_(LangChain).ipynb

```python
summarize_chain: Runnable = (
ChatPromptTemplate.from_messages([
questions_chain: Runnable = (
ChatPromptTemplate.from_messages([
terms_chain: Runnable = (
ChatPromptTemplate.from_messages([
map_chain = RunnableParallel(
"topic": RunnablePassthrough(),  # Pass the original topic through
synthesis_prompt = ChatPromptTemplate.from_messages([
async def run_parallel_example(topic: str) -> None:
```
