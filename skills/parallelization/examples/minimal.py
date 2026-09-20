"""Fan out independent branches concurrently, drop failures, then synthesize.

Real framework: LangChain LCEL RunnableParallel({...}) | synthesis_prompt | llm
  (Google ADK equivalent: ParallelAgent(sub_agents=[...]) followed by a merger agent)
Run: python3 examples/minimal.py
"""

import asyncio


def llm(prompt: str) -> str:
    return f"[canned answer to {prompt!r}]"


async def summarize(topic: str) -> str:
    await asyncio.sleep(0.05)  # stands in for an API round trip
    return llm(f"Summarize: {topic}")


async def questions(topic: str) -> str:
    await asyncio.sleep(0.05)
    return llm(f"Three questions about: {topic}")


async def key_terms(topic: str) -> str:
    await asyncio.sleep(0.05)
    raise RuntimeError("terms branch hit a rate limit")


BRANCHES = {"summary": summarize, "questions": questions, "key_terms": key_terms}


def synthesize(results: dict, missing: list) -> str:
    body = " | ".join(f"{k}={v}" for k, v in results.items())
    return llm(f"Synthesize [{body}] noting missing sources: {missing or 'none'}")


async def run(topic: str) -> str:
    results = await asyncio.gather(*(fn(topic) for fn in BRANCHES.values()),
                                   return_exceptions=True)
    ok, missing = {}, []
    for name, result in zip(BRANCHES, results):
        if isinstance(result, Exception):
            missing.append(name)
            print(f"branch {name}: FAILED ({result})")
        else:
            ok[name] = result
            print(f"branch {name}: ok")
    # Partial failure is explicit: the aggregator still runs and is told what is absent.
    return synthesize(ok, missing)


print("merged:", asyncio.run(run("the history of space exploration")))
