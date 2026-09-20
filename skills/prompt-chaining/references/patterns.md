# Prompt Chaining

Ch 1.

## Frameworks
- LangChain (ChatOpenAI, ChatPromptTemplate, StrOutputParser).

## Key APIs from the notebooks
- `ChatPromptTemplate.from_template('Extract the technical specifications...{text}')`
- `StrOutputParser() to coerce stage outputs to text`
- `LCEL pipe: prompt | llm | parser, then feed result into next prompt`

## Code patterns
- Pattern: decompose -> one prompt per sub-problem -> feed output N as input N+1.
- Prompt template (extract stage): 'Extract the technical specifications from the following text:\n\n{text}'.
- Keep temperature low (0) for deterministic handoffs between stages.

## Prompt templates
- Extract: `Extract the technical specifications from the following text:\n\n{text}`
- Format: `Format the following as a JSON table with fields …: {extract}`
- Summarize: `Summarize for executives in 3 bullets: {table}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_01_Prompt_Chaining_(Code_Example).ipynb`
- `chapter_notebooks/Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`

