# Parallelization

Ch 3.

## Frameworks
- Google ADK (ParallelAgent / LlmAgent researchers); LangChain (RunnableParallel, asyncio).

## Key APIs from the notebooks
- `ADK: researcher_agent_1..N as LlmAgent with narrow instructions ('Output *only* the summary')`
- `LangChain: RunnableParallel + RunnablePassthrough; async run_parallel_example(topic)`
- `asyncio.gather over per-topic chains, then a synthesis chain over joined outputs`

## Code patterns
- Pattern: fan out -> bounded concurrent workers -> join/synthesize.
- Give each worker a narrow instruction and a 1-2 sentence output contract.
- Cap concurrency; add per-branch timeouts before the join.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_03_Parallelization_(Google_ADK).ipynb`
- `chapter_notebooks/Chapter_03_Parallelization_(LangChain).ipynb`

