"""Chapter 9 — Evolutionary adaptation (OpenEvolve). Needs program + evaluator + config."""
from openevolve import OpenEvolve

async def evolve_program(program: str, evaluator: str, config: str, n: int = 100):
    evo = OpenEvolve(
        initial_program_path=program,
        evaluation_file=evaluator,
        config_path=config,
    )
    best = await evo.run(iterations=n)
    return best.metrics
