"""RAG: chunk -> index -> retrieve top-k -> augment prompt -> generate.

Offline stub using word-overlap "embeddings". Swap in a real embedding
model + vector store and an LLM for `generate`; the flow is identical.
"""
import re

DOCS = {
    "policy.md": "Refunds are issued within 14 days. Refund requests need the order id. "
                 "Shipping is free above 50 EUR. Returns must be unused.",
    "faq.md": "Our support hours are 9-17 CET on weekdays. Contact support via chat or email.",
}


def chunk(text: str, size: int = 8, overlap: int = 2) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size - overlap)]


def embed(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


INDEX = [(f"{src}#{i}", c, embed(c)) for src, doc in DOCS.items() for i, c in enumerate(chunk(doc))]


def retrieve(question: str, top_k: int = 2, threshold: int = 1) -> list[tuple[str, str]]:
    q = embed(question)
    scored = sorted(((len(q & e), cid, c) for cid, c, e in INDEX), reverse=True)
    return [(cid, c) for score, cid, c in scored[:top_k] if score >= threshold]


def generate(question: str, context: list[tuple[str, str]]) -> str:
    """Stand-in for an LLM told to answer ONLY from context and cite chunk ids."""
    if not context:
        return "I don't know."
    cid, best = context[0]
    sentence = next((s for s in re.split(r"(?<=\.)\s", best) if embed(s) & embed(question)), best)
    return f"{sentence.strip()} [{cid}]"


def rag(question: str) -> str:
    ctx = retrieve(question)
    prompt = ("Use ONLY the context. If unknown say so.\n"
              f"Question: {question}\nContext:\n" + "\n".join(f"[{cid}] {c}" for cid, c in ctx))
    _ = prompt  # would be sent to the model
    return generate(question, ctx)


if __name__ == "__main__":
    print(rag("How many days for refunds?"))
    print(rag("What are the support hours?"))
    print(rag("Who is the CEO?"))
