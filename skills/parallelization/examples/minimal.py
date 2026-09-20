"""Parallelization — minimal runnable demo (stdlib only)."""
import asyncio

async def research(topic):
    await asyncio.sleep(0.01)
    return f"Finding on {topic}: sources agree it matters."

async def main():
    topics = ["renewables", "batteries", "grids"]
    results = await asyncio.gather(*(research(t) for t in topics))
    print("SYNTHESIS:\n" + "\n".join(f"- {r}" for r in results))

asyncio.run(main())
