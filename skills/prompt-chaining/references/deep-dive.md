# Prompt Chaining — deep dive

Source: Chapter 1 + `chapter_notebooks/Chapter_01_Prompt_Chaining_(Code_Example).ipynb`,
`Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`. Loaded on demand only.
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

## Rule of thumb (SOURCE, GT:L1146–L1149)
Use when a task is too complex for a single prompt, has multiple distinct
processing stages, needs a tool call between steps, or must maintain state
across multi-step reasoning. Also called the Pipeline pattern (GT:L698).

## Why a monolithic prompt fails (SOURCE, GT:L737–L743)
- Instruction neglect: some constraints get dropped.
- Contextual drift: model loses the thread across sub-goals.
- Error propagation: an early mistake compounds.
- Hallucination risk rises with cognitive load.

These are the book's reasons to chain, not risks of chaining. The chain-specific
risk the book names (SOURCE, GT:L771–L774) is the handoff: "If the output of one
prompt is ambiguous or poorly formatted, the subsequent prompt may fail due to
faulty input", mitigated by a structured format such as JSON or XML. Checking
each step's output and not chaining one-shot tasks are DERIVED.

## Core pattern: LCEL two-stage chain
Provenance: SOURCE (abridged) — condensed from GT:L1000–L1036; not verbatim.
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
Provenance: SOURCE (abridged) — condensed from GT:L784–L795 / `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`; `supporting_data` strings shortened.
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

## Typical chain shapes (use-case names SOURCE, GT:L810–L955; stage lists DERIVED)
| Shape | Stages |
|---|---|
| Information workflow | summarise -> extract entities -> query DB -> draft report |
| Content generation | brainstorm -> outline -> draft -> revise |
| Conversational | classify intent -> extract slots -> lookup -> respond |
| Code generation | pseudocode -> implement -> unit tests -> fix |
| Data processing | parse -> validate -> transform -> load |

## Context engineering notes (SOURCE, GT:L1068–L1080)
The chapter frames chaining as part of *context engineering*: at each stage
you control exactly what the model sees (system prompt, retrieved docs, tool
outputs, prior state). Pass only what the next stage needs.

## Framework mapping (DERIVED: Ch 1 names LangChain, LangGraph, Crew AI and Google ADK at GT:L972 but shows only LangChain code)
- LangChain/LangGraph: LCEL `|` pipes; LangGraph for cycles or state.
- Google ADK: `SequentialAgent(sub_agents=[a, b])`; stage output via `output_key`
  and read from `state['<key>']` in the next agent's instruction.
- CrewAI: `Task(context=[previous_task])`.

## Debugging checklist (DERIVED)
- Print every intermediate output; most failures are at a boundary.
- If stage N+1 misreads stage N, force a schema (JSON) at the boundary.
- Cap chain length; 3-5 stages is typical. Longer chains want `planning`.

## Pattern variants (DERIVED summary; book terms cited where present)
- **Linear pipeline** — fixed stages, each output piped into the next prompt; wins when the decomposition is known up front.
- **Structured handoff** — stages exchange JSON (e.g. `{"trends": [{"trend_name", "supporting_data"}]}`) instead of prose; wins when the next stage must parse, not read.
- **Tool-interleaved chain** — non-LLM work (parse, DB lookup, validation) sits between prompts; wins when a stage needs ground truth rather than recall.
- **Stateful chain (LangGraph)** — intermediates live in a graph state object instead of a single pipe; wins when you need branching, retries, or loops.
- **Conversational chain** — each turn extracts intent and entities into state, and the next prompt is rebuilt from accumulated state; wins for multi-turn dialogue.

## More prompt templates
Provenance: SOURCE — lines found verbatim in GT:L1018–L1018.
```text
Extract the technical specifications from the following text:

{text_input}
```

Provenance: SOURCE — lines found verbatim in GT:L1024–L1025.
```text
Transform the following specifications into a JSON object with 'cpu',
'memory', and 'storage' as keys:

{specifications}
```

## Framework notes (DERIVED except where cited)
- **LangChain / LangGraph** — LCEL `|` composes stateless linear chains; LangGraph adds a persistent state object for cyclic or conditional chains.
- **Google ADK** — stages are `LlmAgent`s under a `SequentialAgent`; each writes to `session.state` via `output_key` and the next reads it by key.
- **CrewAI / other** — named in the chapter (GT:L972) with no code example.

## Failure modes in depth (DERIVED)
- **Silent early-stage error** — stage 2 cannot distinguish a bad extraction from a good one, so it reformats garbage confidently. Validate each stage's output against its schema and fail loudly instead of passing through.
- **Unparsed free text between stages** — `StrOutputParser()` hands raw prose to the next `ChatPromptTemplate`, whose placeholder expects a specific shape. Fix a per-stage schema and parse (JSON / Pydantic) before the handoff.
- **Linear latency and cost** — every stage is a full round trip, so an N-stage chain costs N calls. Merge stages that do not need separate focus, and cache or precompute deterministic ones.
- **Lost context** — only the previous output is piped forward, so stage 3 never sees the original input. Carry originals explicitly with `RunnablePassthrough` or a state dict keyed per stage.
