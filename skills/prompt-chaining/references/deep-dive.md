# Prompt Chaining — deep dive

Source: Chapter 1 + `chapter_notebooks/Chapter_01_Prompt_Chaining_(Code_Example).ipynb`,
`Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`. Loaded on demand only.

## Rule of thumb (book)
Use when a task is too complex for a single prompt, has multiple distinct
processing stages, needs a tool call between steps, or must maintain state
across multi-step reasoning. Also called the Pipeline pattern.

## Why a monolithic prompt fails
- Instruction neglect: some constraints get dropped.
- Contextual drift: model loses the thread across sub-goals.
- Error propagation: an early mistake compounds.
- Hallucination risk rises with cognitive load.

## Core pattern: LCEL two-stage chain
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)

prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}")
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with "
    "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}")

extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = ({"specifications": extraction_chain} | prompt_transform | llm | StrOutputParser())

result = full_chain.invoke({"text_input": "3.5 GHz octa-core, 16GB RAM, 1TB NVMe SSD."})
```
Key mechanics:
- `{"specifications": extraction_chain}` maps stage-1 output onto the stage-2 input variable.
- `StrOutputParser()` normalises the message to a string between stages.
- `temperature=0` keeps handoffs deterministic.

## Structured handoff (JSON example)
Have each stage emit a fixed schema so the next prompt can rely on it:
```json
{
  "trends": [
    {"trend_name": "AI-Powered Personalization",
     "supporting_data": "73% of consumers prefer brands that personalise."},
    {"trend_name": "Sustainable and Ethical Brands",
     "supporting_data": "ESG-claim products grew 28% vs 20%."}
  ]
}
```
Downstream prompts then reference `{trends}` rather than parsing prose.

## Typical chain shapes
| Shape | Stages |
|---|---|
| Information workflow | summarise -> extract entities -> query DB -> draft report |
| Content generation | brainstorm -> outline -> draft -> revise |
| Conversational | classify intent -> extract slots -> lookup -> respond |
| Code generation | pseudocode -> implement -> unit tests -> fix |
| Data processing | parse -> validate -> transform -> load |

## Context engineering notes
The chapter frames chaining as part of *context engineering*: at each stage
you control exactly what the model sees (system prompt, retrieved docs, tool
outputs, prior state). Pass only what the next stage needs.

## Framework mapping
- LangChain/LangGraph: LCEL `|` pipes; LangGraph for cycles or state.
- Google ADK: `SequentialAgent(sub_agents=[a, b])`; stage output via `output_key`
  and read from `state['<key>']` in the next agent's instruction.
- CrewAI: `Task(context=[previous_task])`.

## Debugging checklist
- Print every intermediate output; most failures are at a boundary.
- If stage N+1 misreads stage N, force a schema (JSON) at the boundary.
- Cap chain length; 3-5 stages is typical. Longer chains want `planning`.

## Pattern variants
- **Linear pipeline** — fixed stages, each output piped into the next prompt; wins when the decomposition is known up front.
- **Structured handoff** — stages exchange JSON (e.g. `{"trends": [{"trend_name", "supporting_data"}]}`) instead of prose; wins when the next stage must parse, not read.
- **Tool-interleaved chain** — non-LLM work (parse, DB lookup, validation) sits between prompts; wins when a stage needs ground truth rather than recall.
- **Stateful chain (LangGraph)** — intermediates live in a graph state object instead of a single pipe; wins when you need branching, retries, or loops.
- **Conversational chain** — each turn extracts intent and entities into state, and the next prompt is rebuilt from accumulated state; wins for multi-turn dialogue.

## More prompt templates
```text
Extract the technical specifications from the following text:

{text_input}
```

```text
Transform the following specifications into a JSON object with 'cpu',
'memory', and 'storage' as keys:

{specifications}
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
