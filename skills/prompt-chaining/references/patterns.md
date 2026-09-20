# Prompt Chaining — patterns (Ch 1)

## Pattern
1. Split the task into stages with one job each.
2. Make every stage emit a structured handoff (JSON or fixed fields).
3. Pipe stage N output into stage N+1 prompt variables.
4. Validate or transform between stages when needed.

## Prompt template
```
Stage 1: Extract the technical specifications from the following text:
{text_input}
Stage 2: Transform the following specifications into a JSON object with
'cpu', 'memory' and 'storage' as keys:
{specifications}
```

## Key APIs
- LangChain LCEL: `prompt | llm | StrOutputParser()`; `{"specifications": chain1} | chain2`.
- `llm.with_structured_output(PydanticModel)` for typed handoffs.
- ADK: `SequentialAgent(sub_agents=[...])`, each with `output_key`, read via `{key}`.

## Pitfalls -> fixes
- Free-text handoff -> require JSON and parse it.
- Lost early context -> pass original input through with `RunnablePassthrough`.
- Silent stage failure -> log each stage output; fail fast.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_01_*`.
