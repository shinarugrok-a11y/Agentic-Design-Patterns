"""Chapter 1 — Prompt chaining (LangChain LCEL). Requires OPENAI_API_KEY."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)
extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from:\n\n{text_input}"
) | llm | StrOutputParser()
chain = (
    {"specifications": extract}
    | ChatPromptTemplate.from_template(
        "JSON with keys cpu, memory, storage:\n\n{specifications}"
    )
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    print(chain.invoke({"text_input": "3.5 GHz octa-core, 16GB RAM, 1TB NVMe SSD."}))
