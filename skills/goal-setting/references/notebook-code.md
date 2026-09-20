# Goal Setting and Monitoring — reference patterns

Source: Chapter 11 + `Chapter_11_Goal_Setting_(Iteration).ipynb` (Mahtab Syed, MIT).

## Rule of thumb (book)
Use when an agent must autonomously execute a multi-step task, adapt to
dynamic conditions and reliably reach a specific high-level objective
without constant human intervention. Goals should be SMART (specific,
measurable, achievable, relevant, time-bound). Monitoring observes agent
actions, environment state and tool outputs; the feedback loop lets the
agent revise, adapt or escalate. In ADK, goals live in agent instructions
and monitoring is done through state and tool interactions.

## Notebook architecture: goal-driven code agent
```
use_case + goals
   -> generate_prompt(use_case, goals, previous_code, feedback)
   -> llm -> code
   -> get_code_feedback(code, goals)        # critic
   -> goals_met(feedback, goals) -> bool    # judge, strict True/False
   -> stop | loop (max_iterations=5)
   -> add_comment_header -> save_code_to_file
```

### Generation prompt
```python
base_prompt = f"""
You are an AI coding agent. Your job is to write Python code based on the following use case:

Use Case: {use_case}

Your goals are:
{chr(10).join(f"- {g.strip()}" for g in goals)}
"""
if previous_code: base_prompt += f"\nPreviously generated code:\n{previous_code}"
if feedback:      base_prompt += f"\nFeedback on previous version:\n{feedback}\n"
base_prompt += "\nPlease return only the revised Python code. Do not include comments or explanations outside the code."
```

### Feedback (monitor) prompt
```python
feedback_prompt = f"""
You are a Python code reviewer. A code snippet is shown below. Based on the following goals:

{chr(10).join(f"- {g.strip()}" for g in goals)}

Please critique this code and identify if the goals are met. Mention if improvements are needed for clarity, simplicity, correctness, edge case handling, or test coverage.

Code:
{code}
"""
```

### Judge prompt (boolean stop condition)
```python
review_prompt = f"""
You are an AI reviewer.

Here are the goals:
{chr(10).join(f"- {g.strip()}" for g in goals)}

Here is the feedback on the code:
\"\"\"
{feedback_text}
\"\"\"

Based on the feedback above, have the goals been met?

Respond with only one word: True or False.
"""
return llm.invoke(review_prompt).content.strip().lower() == "true"
```

### Loop
```python
for i in range(max_iterations):
    code = clean_code_block(llm.invoke(generate_prompt(use_case, goals, previous_code, feedback)).content)
    feedback = get_code_feedback(code, goals).content.strip()
    if goals_met(feedback, goals):
        break
    previous_code = code
final = add_comment_header(code, use_case)
save_code_to_file(final, use_case)      # llm-derived short filename + random suffix
```
Helpers: `clean_code_block` strips ``` fences; `to_snake_case`; filename
from an LLM summary (<=10 chars) plus a 4-digit suffix.

### Example goals used
"Code simple to understand, Functionally correct, Handles comprehensive edge
cases, Takes positive integer input only, prints the results with few examples"

## Design notes
- Separate *feedback* (rich critique) from *judgment* (strict boolean); the
  boolean makes termination reliable.
- Restate goals in every prompt; do not rely on history.
- Report unmet goals when the iteration cap is hit rather than saving silently.
- Goals that conflict ("simple" vs "comprehensive edge cases") need priority
  ordering (see `prioritization`).

## Monitoring signals beyond LLM judgment
Unit tests, schema validation, latency/cost counters, tool return codes,
state flags (`state["status"] == "completed"`). Prefer deterministic checks
when available; use the LLM judge for qualitative goals.
