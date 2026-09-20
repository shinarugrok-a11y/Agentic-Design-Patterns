---
name: reasoning-techniques
description: Apply structured reasoning: chain-of-thought, self-correction, code execution.
role: [critic]
chapter: 17
token_cost_estimate: 209
chains_with: [reflection, tool-use]
---

# Reasoning Techniques

## When to use
- Problem needs math, logic, or multi-hop inference.
- Pick: CoT prompt, self-correction loop, or code execution.
- Verify intermediate steps, not just the final answer.

## When NOT to use
- Simple lookup or creative style task.
- Verbose traces leak into user-facing output.

## Inputs
- Problem + chosen technique
- Verifier for steps or final answer

## Outputs
- Answer + reasoning trace

## Failure modes
- CoT rationalizes a wrong answer convincingly.
- Self-correction flips right answers to wrong ones.
- Code executor runs untrusted code without sandboxing.

## Minimal example
```python
trace = llm(f"Think step by step: {problem}")
answer = llm(f"Given trace {trace}, final answer only.")
check_with_code(answer)
```

## Next skills
- If reasoning needs iterative critique: load `reflection`
- If verification needs execution or search: load `tool-use`
