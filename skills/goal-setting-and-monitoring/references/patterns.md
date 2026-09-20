# Goal Setting and Monitoring — Patterns

## Pattern variants
- **Generate → critique → binary judge** — a generator produces the artifact, a reviewer critiques it against the goal list, a third call answers only `True`/`False`; wins when success is subjective but describable, because the judge gives the loop a parsable stop condition.
- **Checklist goal object** — `{objective, done_when: [...], max_steps}` with machine-checkable predicates; wins when criteria are observable facts and no LLM judge is needed.
- **Per-step monitoring** — re-evaluate after every action instead of once at the end, feeding the critique back into the next generation prompt; wins for long autonomous runs where drift compounds.
- **Threshold / risk monitor** — track a metric against a tolerance (portfolio risk, false-positive rate, milestone date) and act when it is breached rather than when the goal fails.
- **Escalate on non-convergence** — when the budget is exhausted with criteria unmet, hand off to a human with the unmet list; wins over emitting an unverified "done".

## Prompt templates

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

## Code patterns

LangChain (`ChatOpenAI`, plain `llm.invoke`; the monitor loop is ordinary Python):
```python
for i in range(max_iterations):                     # hard budget, 5 in the notebook
    prompt = generate_prompt(use_case, goals, previous_code, feedback)
    code = clean_code_block(llm.invoke(prompt).content.strip())
    feedback = get_code_feedback(code, goals)       # critique every iteration
    if goals_met(feedback.content.strip(), goals):  # judge, not the generator
        break
    previous_code = code
save_code_to_file(add_comment_header(code, use_case), use_case)
```

Parsing the judge into a hard boolean:
```python
def goals_met(feedback_text: str, goals: list[str]) -> bool:
    response = llm.invoke(review_prompt).content.strip().lower()
    return response == "true"      # anything else keeps the loop running
```

## Framework notes
- **LangChain / LangGraph** — `ChatOpenAI(model="gpt-4o", temperature=0.3)` with three distinct `invoke` calls (generate, critique, judge); no chain object is used, the loop is a `for` in Python.
- **Google ADK** — not used in this chapter.

## Failure modes in depth
- **Unmeasurable goals** — goals like "handles comprehensive edge cases" cannot terminate a loop on their own. Force the judge into one word and compare `== "true"`, so ambiguity keeps iterating instead of falsely stopping.
- **Monitoring only at the end** — run the critique inside every iteration and append it to the next generation prompt; late detection leaves no budget to correct.
- **Success declared without verification** — never let the call that produced the artifact also rule on it. Keep the generator, reviewer, and judge as separate calls with separate prompts.
- **No budget, so the loop never ends** — cap with `max_iterations` (and a wall clock for long runs); on exhaustion return the last artifact plus the unmet criteria rather than a success verdict.

## Source
Chapter 11 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_11_Goal_Setting_(Iteration).ipynb.
