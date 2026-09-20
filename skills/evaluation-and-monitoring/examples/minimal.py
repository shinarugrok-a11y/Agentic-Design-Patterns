"""Scores an evalset on output match, trajectory diff, tokens, and latency drift.

Real framework: Google ADK AgentEvaluator.evaluate(agent_module, eval_dataset_
file_path_or_dir), the same check `adk eval` runs over a .evalset.json file.
Run: python3 examples/minimal.py
"""
import time

EVALSET = [
    {"id": "weather", "input": "weather in Rome?", "expected": "Rome: 21C",
     "ideal_steps": ["parse", "get_weather"]},
    {"id": "math", "input": "what is 2+2?", "expected": "4",
     "ideal_steps": ["compute"]},
]
BASELINE = {"weather": {"match": 1.0, "trajectory": 1.0},
            "math": {"match": 1.0, "trajectory": 1.0}}


def llm(prompt: str):
    """Canned agent: returns (answer, tool trajectory)."""
    if "weather" in prompt:
        return "Rome: 21C", ["parse", "get_weather"]
    return "4", ["search_web", "compute"]      # extra, unnecessary step


def score(out, expected):
    return 1.0 if out.strip().lower() == expected.strip().lower() else 0.0


def traj_diff(actual, ideal):
    return 1.0 if actual == ideal else round(
        len([s for s in ideal if s in actual]) / len(ideal) - 0.5, 2)


for case in EVALSET:
    start = time.perf_counter()
    out, traj = llm(case["input"])
    scores = {"match": score(out, case["expected"]),
              "trajectory": traj_diff(traj, case["ideal_steps"]),
              "tokens": len(case["input"].split()) + len(out.split()),
              "latency_ms": round((time.perf_counter() - start) * 1000, 3)}
    print(f"{case['id']}: {scores}")
    for metric, base in BASELINE[case["id"]].items():
        if scores[metric] < base:
            print(f"  DRIFT on {metric}: {scores[metric]} < baseline {base}"
                  f" (trajectory was {traj}, ideal {case['ideal_steps']})")
