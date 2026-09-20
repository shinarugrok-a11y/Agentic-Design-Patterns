"""Chapter 3 — Parallel independent chains, then synthesize (grounded merge)."""
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def build(llm, summarize, questions, terms, synthesis_prompt):
    mapped = RunnableParallel(
        summary=summarize,
        questions=questions,
        key_terms=terms,
        topic=RunnablePassthrough(),
    )
    return mapped | synthesis_prompt | llm | StrOutputParser()
