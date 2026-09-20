---
name: reasoning-techniques
description: CoT, ToT, self-correction, ReAct and debate to make thinking explicit. Force step-by-step reasoning, multiple candidate paths, or a think-act-observe loop when a direct answer is unreliable. Do not use for lookups or formatting tasks where extra reasoning tokens add cost without accuracy.
role: [critic]
chapter: 17
token_cost_estimate: 330
chains_with: [reflection, tool-use, planning]
---

# Reasoning Techniques

## When to use
- Multi-step logic, math, or decomposition.
- Showing work matters for trust/audit.
- Need to explore and backtrack among strategies (ToT).
- Reasoning must interleave with tool calls (ReAct).

## When NOT to use
- Simple retrieval or rewrite.
- Latency-critical path.
- Model already uses hidden reasoning; explicit CoT duplicates it.

## Inputs
- Problem statement
- Reasoning template (steps)
- Tools for ReAct
- Thinking budget

## Outputs
- Explicit thought trace
- Final answer
- Revised answer after self-correction

## Failure modes
- Confident wrong chain; steps look valid but premise is false.
- ToT branching explodes token cost.
- ReAct loop repeats the same action.
- Self-correction rewrites correct content.

## Minimal example
```python
COT = """1. Analyze the query  2. Formulate search queries
3. Simulate retrieval  4. Synthesize  5. Review and refine
Show each thought, then give the final answer."""
answer = llm(COT + query)
# ReAct graph: generate_query -> web_research -> reflection -(more?)-> web_research | finalize
# Self-correction: understand reqs -> analyse draft -> list gaps -> propose fixes -> rewrite
```

## Next skills
- If need an external critic loop: load `reflection`
- If ReAct actions are tool calls: load `tool-use`
- If reasoning should produce a plan: load `planning`
