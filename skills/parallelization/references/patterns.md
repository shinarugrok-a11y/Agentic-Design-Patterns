# Parallelization — Pattern reference

Load this file only when implementing `parallelization`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when independent operations can run at once (multi-API fetch, chunk processing, multi-view generation then merge).

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Example of parallelization with sub-agents. Fig. 2: Parallelization design pattern.

## Notebooks (extracted)

Parallelization

### Notebooks
- `Chapter_03_Parallelization_(Google_ADK).ipynb`
- `Chapter_03_Parallelization_(LangChain).ipynb`

### Patterns
- **ADK:** `ParallelAgent` runs sub-agents concurrently; each uses `output_key` → state; `SequentialAgent` chains parallel block then merger
- **LangChain:** `RunnableParallel` runs summarize / questions / terms chains; synthesis prompt merges results
- **Merger grounding:** synthesis agent must use only parallel outputs (no external knowledge)

### Prompt templates
Merger instruction (ADK) — key constraint:
```
**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**
```

LangChain synthesis system prompt:
```
Based on the following information:
 Summary: {summary}
 Related Questions: {questions}
 Key Terms: {key_terms}
 Synthesize a comprehensive answer.
```

### Minimal code
```python
# LangChain parallel + synthesis
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

map_chain = RunnableParallel(
    summary=summarize_chain,
    questions=questions_chain,
    key_terms=terms_chain,
    topic=RunnablePassthrough(),
)
full_chain = map_chain | synthesis_prompt | llm | StrOutputParser()
await full_chain.ainvoke("The history of space exploration")
```

```python
# ADK pattern (fragment)
parallel_research = ParallelAgent(name="ParallelWebResearchAgent", sub_agents=[r1, r2, r3])
pipeline = SequentialAgent(name="ResearchAndSynthesisPipeline", sub_agents=[parallel_research, merger_agent])
```

### Caveats
- ADK snippet is partial — requires full `agent.py` setup per ADK quickstart
- LangChain example uses `async`/`ainvoke`
- ADK researchers depend on `google_search` tool and `GEMINI_MODEL` constant defined elsewhere

---

## Failure modes (skill-level)
- Merger invents facts not in worker outputs
- Fan-out without join loses results
- Shared mutable state races

## Chains with
`routing`, `prompt-chaining`
