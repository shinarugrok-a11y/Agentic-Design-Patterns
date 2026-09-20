"""Chapter 2 — Routing. Classifier emits one label; branch to a specialist."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

# llm = your chat model
def booking_handler(req: str) -> str: return f"[booker] {req}"
def info_handler(req: str) -> str: return f"[info] {req}"
def unclear_handler(req: str) -> str: return "[unclear] please rephrase"

def build(llm):
    router = ChatPromptTemplate.from_messages([
        ("system", "Output ONLY one word: booker, info, or unclear."),
        ("user", "{request}"),
    ]) | llm | StrOutputParser()
    branch = RunnableBranch(
        (lambda x: "booker" in x["decision"].lower(), lambda x: booking_handler(x["request"])),
        (lambda x: "info" in x["decision"].lower(), lambda x: info_handler(x["request"])),
        lambda x: unclear_handler(x["request"]),
    )
    return {"decision": router, "request": RunnablePassthrough()} | branch
