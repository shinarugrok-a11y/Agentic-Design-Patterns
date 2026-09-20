"""Minimal example: Knowledge Retrieval (RAG) (Ch 14). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    chunks = retrieve(query, top_k=5)  # vector or search
    answer = run(f"Answer {query} using only: {chunks}")
    return with_citations(answer, chunks)


if __name__ == "__main__":
    print(main())
