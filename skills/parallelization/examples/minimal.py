"""Parallelization: fan out independent branches, join, then synthesise.

Offline stub. Replace `branch_*` with real LLM/tool coroutines; the shape
(asyncio.gather -> keyed results -> synthesis) stays the same.
"""
import asyncio


async def branch_summary(topic: str) -> str:
    await asyncio.sleep(0.2)
    return f"Summary of {topic}."


async def branch_questions(topic: str) -> str:
    await asyncio.sleep(0.2)
    return f"Q1/Q2/Q3 about {topic}."


async def branch_terms(topic: str) -> str:
    await asyncio.sleep(0.2)
    return "term-a, term-b, term-c"


def synthesise(results: dict) -> str:
    # In production this is an LLM prompt told to ground ONLY on `results`.
    return ("## Report\n"
            f"- Summary: {results['summary']}\n"
            f"- Questions: {results['questions']}\n"
            f"- Key terms: {results['key_terms']}\n"
            f"- Topic: {results['topic']}")


async def run(topic: str) -> str:
    summary, questions, terms = await asyncio.gather(
        branch_summary(topic), branch_questions(topic), branch_terms(topic))
    results = {"summary": summary, "questions": questions, "key_terms": terms, "topic": topic}
    return synthesise(results)


if __name__ == "__main__":
    print(asyncio.run(run("The history of space exploration")))
