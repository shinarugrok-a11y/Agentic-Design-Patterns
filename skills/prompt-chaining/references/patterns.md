# Prompt Chaining — Patterns

## Pattern variants
- **Linear pipeline** — fixed stages, each output piped into the next prompt; wins when the decomposition is known up front.
- **Structured handoff** — stages exchange JSON (e.g. `{"trends": [{"trend_name", "supporting_data"}]}`) instead of prose; wins when the next stage must parse, not read.
- **Tool-interleaved chain** — non-LLM work (parse, DB lookup, validation) sits between prompts; wins when a stage needs ground truth rather than recall.
- **Stateful chain (LangGraph)** — intermediates live in a graph state object instead of a single pipe; wins when you need branching, retries, or loops.
- **Conversational chain** — each turn extracts intent and entities into state, and the next prompt is rebuilt from accumulated state; wins for multi-turn dialogue.

## Prompt templates

```text
Extract the technical specifications from the following text:

{text_input}
```

```text
Transform the following specifications into a JSON object with 'cpu',
'memory', and 'storage' as keys:

{specifications}
```

## Code patterns

LangChain (LCEL):

```python
extraction_chain = prompt_extract | llm | StrOutputParser()

# The dict key names the variable prompt_transform expects — this is the handoff.
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

final_result = full_chain.invoke({"text_input": input_text})
```

## Framework notes
- **LangChain / LangGraph** — LCEL `|` composes stateless linear chains; LangGraph adds a persistent state object for cyclic or conditional chains.
- **Google ADK** — stages are `LlmAgent`s under a `SequentialAgent`; each writes to `session.state` via `output_key` and the next reads it by key.
- **CrewAI / other** — named in the chapter as an alternative orchestrator for multi-step sequences; no code example accompanies it.

## Failure modes in depth
- **Silent early-stage error** — stage 2 cannot distinguish a bad extraction from a good one, so it reformats garbage confidently. Validate each stage's output against its schema and fail loudly instead of passing through.
- **Unparsed free text between stages** — `StrOutputParser()` hands raw prose to the next `ChatPromptTemplate`, whose placeholder expects a specific shape. Fix a per-stage schema and parse (JSON / Pydantic) before the handoff.
- **Linear latency and cost** — every stage is a full round trip, so an N-stage chain costs N calls. Merge stages that do not need separate focus, and cache or precompute deterministic ones.
- **Lost context** — only the previous output is piped forward, so stage 3 never sees the original input. Carry originals explicitly with `RunnablePassthrough` or a state dict keyed per stage.

## Source
Chapter 1 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_01_Prompt_Chaining_(Code_Example).ipynb, Chapter_01_Prompt_Chaining_(JSON_Example).ipynb.
