"""Retrieve top-k chunks, ground the answer in them, and cite the sources used.

Real framework: LangChain retriever.invoke(query) feeding
ChatPromptTemplate.from_template(RAG_PROMPT) | llm | StrOutputParser().
Run: python3 examples/minimal.py
"""

CORPUS = [
    {"source": "hr_policy_2025.md", "text": "Remote work is allowed three days a week."},
    {"source": "blog_2020.md", "text": "Remote work was a temporary pandemic measure."},
    {"source": "expenses.md", "text": "Travel expenses require a receipt over 25 EUR."},
]
RAG_PROMPT = ("Use the retrieved context to answer. If the context does not contain "
              "the answer, say you don't know.\nContext: {context}\nQuestion: {question}")


STOP = {"what", "is", "the", "a", "of", "for", "my"}


def terms(text):
    return {w.strip("?.,") for w in text.lower().split()} - STOP


def retrieve(query, k=2):
    """Fake vector search: score chunks by shared content words, keep the top k."""
    scored = [(len(terms(query) & terms(d["text"])), d) for d in CORPUS]
    hits = [d for score, d in sorted(scored, key=lambda p: -p[0]) if score]
    return hits[:k]


def llm(prompt: str) -> str:
    """Fake generator: answers only from the context block it was handed."""
    context = prompt.split("Context: ")[1].split("\nQuestion")[0]
    if "three days" in context:
        return "Remote work is allowed three days a week."
    return "I don't know."


def answer(question: str) -> str:
    docs = retrieve(question)
    if not docs:
        return "I don't know. (nothing retrieved)"
    context = "\n\n".join(f"[{i}] {d['text']}" for i, d in enumerate(docs))
    text = llm(RAG_PROMPT.format(context=context, question=question))
    cites = ", ".join(f"[{i}] {d['source']}" for i, d in enumerate(docs))
    return f"{text}\nsources: {cites}"


for q in ["What is the remote work policy?", "What is the parking policy?"]:
    print(f"Q: {q}\nA: {answer(q)}\n")
