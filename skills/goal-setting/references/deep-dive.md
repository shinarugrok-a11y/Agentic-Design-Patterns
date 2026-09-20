# Goal Setting and Monitoring — deep dive

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

## Pattern variants
- **Generate → critique → binary judge** — a generator produces the artifact, a reviewer critiques it against the goal list, a third call answers only `True`/`False`; wins when success is subjective but describable, because the judge gives the loop a parsable stop condition.
- **Checklist goal object** — `{objective, done_when: [...], max_steps}` with machine-checkable predicates; wins when criteria are observable facts and no LLM judge is needed.
- **Per-step monitoring** — re-evaluate after every action instead of once at the end, feeding the critique back into the next generation prompt; wins for long autonomous runs where drift compounds.
- **Threshold / risk monitor** — track a metric against a tolerance (portfolio risk, false-positive rate, milestone date) and act when it is breached rather than when the goal fails.
- **Escalate on non-convergence** — when the budget is exhausted with criteria unmet, hand off to a human with the unmet list; wins over emitting an unverified "done".

## More prompt templates
Generation, carrying the previous attempt and its critique:
```
You are an AI coding agent. Your job is to write Python code based on the following use case:

Use Case: {use_case}

Your goals are:
- {goal_1}
- {goal_2}

Previously generated code:
{previous_code}
Feedback on previous version:
{feedback}

Please return only the revised Python code. Do not include comments or explanations
outside the code.
```

Critique against the goals (separate call from the generator):
```
You are a Python code reviewer. A code snippet is shown below. Based on the following goals:
- {goal_1}
Please critique this code and identify if the goals are met. Mention if improvements are
needed for clarity, simplicity, correctness, edge case handling, or test coverage.

Code:
{code}
```

Binary judge — the stop condition:
```
You are an AI reviewer.
Here are the goals:
- {goal_1}
Here is the feedback on the code:
"""{feedback_text}"""
Based on the feedback above, have the goals been met?
Respond with only one word: True or False.
```

## Framework notes
- **LangChain / LangGraph** — `ChatOpenAI(model="gpt-4o", temperature=0.3)` with three distinct `invoke` calls (generate, critique, judge); no chain object is used, the loop is a `for` in Python.
- **Google ADK** — not used in this chapter.

## Failure modes in depth
- **Unmeasurable goals** — goals like "handles comprehensive edge cases" cannot terminate a loop on their own. Force the judge into one word and compare `== "true"`, so ambiguity keeps iterating instead of falsely stopping.
- **Monitoring only at the end** — run the critique inside every iteration and append it to the next generation prompt; late detection leaves no budget to correct.
- **Success declared without verification** — never let the call that produced the artifact also rule on it. Keep the generator, reviewer, and judge as separate calls with separate prompts.
- **No budget, so the loop never ends** — cap with `max_iterations` (and a wall clock for long runs); on exhaustion return the last artifact plus the unmet criteria rather than a success verdict.
