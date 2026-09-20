# Prompt Chaining patterns (Ch 1)

Two notebook variants: LangChain `ChatPromptTemplate | StrOutputParser` chain (Code Example) and JSON-schema chaining (JSON Example).

Pattern A — LangChain chain: `ChatOpenAI(temperature=0)` + `ChatPromptTemplate` per stage + `StrOutputParser`, composed with `|` so stage output feeds the next prompt. Used for extract-then-summarize flows.

Pattern B — JSON contract chaining: stage 1 emits strict JSON (`trends: [{trend_name, supporting_data}]`); stage 2 consumes that JSON. Enforce the schema between stages; reject and retry on parse failure.

Prompt templates: stage prompts are narrow and single-purpose ("Extract information…", "Summarize…"). Keep temperature 0 for extract/transform stages, raise only for creative final stages.

Rule of thumb: cap chains at 3-5 stages; add a validation gate (schema check) after every untrusted stage.

## Notebook extracts (on-demand detail)

### Chapter_01_Prompt_Chaining_(Code_Example).ipynb

```python
# --- Prompt 1: Extract Information ---
prompt_extract = ChatPromptTemplate.from_template(
# --- Prompt 2: Transform to JSON ---
prompt_transform = ChatPromptTemplate.from_template(
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# For better security, load environment variables from a .env file
# Initialize the Language Model (using ChatOpenAI is recommended)
# The StrOutputParser() converts the LLM's message output to a simple string.
```

### Chapter_01_Prompt_Chaining_(JSON_Example).ipynb

```python
(boilerplate-only notebook; see .ipynb)
```
