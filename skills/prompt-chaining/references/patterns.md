# Prompt Chaining — Pattern reference

Load this file only when implementing `prompt-chaining`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when a task is too complex for a single prompt, has distinct stages, needs tools between steps, or must keep staged state.

## Book — visual (figure captions; images stay in the PDF)
Fig. 2: Prompt Chaining Pattern — Agents receive a series of prompts; each agent's output is the next agent's input.

## Notebooks (extracted)

Prompt Chaining

### Notebooks
- `Chapter_01_Prompt_Chaining_(Code_Example).ipynb`
- `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`

### Patterns
- **Framework:** LangChain LCEL (`ChatPromptTemplate | llm | StrOutputParser`)
- **Two-stage chain:** extract specs → transform to JSON via dict passthrough
- **Intermediate binding:** `{"specifications": extraction_chain}` feeds prior output into next prompt
- **JSON example notebook:** sample structured output (not executable Python)

### Prompt templates
```
Extract the technical specifications from the following text:

{text_input}
```
```
Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:

{specifications}
```

### Minimal code
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)

prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with "
    "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

result = full_chain.invoke({"text_input": "3.5 GHz octa-core, 16GB RAM, 1TB NVMe SSD."})
```

### Caveats
- Requires `OPENAI_API_KEY` (optionally via `.env` / `dotenv`)
- `JSON_Example` notebook is reference output only — not runnable code
- Use `temperature=0` for deterministic structured extraction

---

## Failure modes (skill-level)
- Error compounding across stages
- Unstructured intermediates lose fields
- Over-chaining adds latency without quality

## Chains with
`routing`, `tool-use`
