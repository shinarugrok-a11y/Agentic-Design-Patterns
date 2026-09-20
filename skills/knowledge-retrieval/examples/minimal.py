"""Knowledge Retrieval (RAG) — minimal runnable demo (stdlib only)."""
DOCS = ["Refunds allowed within 30 days.", "Shipping takes 3-5 days.", "Warranty covers 1 year."]

def retrieve(q, k=2):
    scored = sorted(DOCS, key=lambda d: len(set(q.lower().split()) & set(d.lower().split())), reverse=True)
    return scored[:k]

q = "How long for a refund?"
print("SOURCES:", retrieve(q))
print("ANSWER (grounded):", " ".join(retrieve(q)[:1]))
