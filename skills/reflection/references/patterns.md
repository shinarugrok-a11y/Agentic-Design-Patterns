# Reflection — Patterns

## Pattern variants
- **Single-pass generate-critique-refine** — one fixed round of draft, critique, rewrite; wins when quality matters but the cost ceiling is a known 3 calls.
- **Iterative loop with stop phrase** — repeat until the critic emits a sentinel (`CODE_IS_PERFECT`) or `max_iterations` is hit; wins for code and long-form text that converge over rounds.
- **Producer-Critic (separate agents)** — a distinct critic agent with its own role and rubric judges the producer's output; wins on high-stakes or specialist evaluation where self-review is too lenient.
- **Structured-verdict critique** — the critic returns `{"status": "ACCURATE"|"INACCURATE", "reasoning": ...}` instead of prose; wins when control flow must branch on the verdict.
- **Tool-grounded reflection** — critique comes from running tests, a linter, or static analysis rather than from a model; wins whenever an objective oracle exists.

## Prompt templates

Critic with an explicit stop phrase:

```text
You are a senior software engineer and an expert in Python. Perform a
meticulous code review. Critically evaluate the provided code against the
original task requirements. Look for bugs, style issues, missing edge cases,
and areas for improvement.

If the code is perfect and meets all requirements, respond with the single
phrase 'CODE_IS_PERFECT'. Otherwise, provide a bulleted list of critiques.

Original Task:
{task_prompt}

Code to Review:
{current_code}
```

Critic with a machine-readable verdict:

```text
You are a meticulous fact-checker.
1. Read the text provided in the state key 'draft_text'.
2. Carefully verify the factual accuracy of all claims.
3. Your final output must be a dictionary containing two keys:
   - "status": either "ACCURATE" or "INACCURATE".
   - "reasoning": a clear explanation, citing specific issues if any.
```

## Code patterns

LangChain (LCEL, single pass):

```python
full_reflection_chain = (
    RunnablePassthrough.assign(initial_description=generation_chain)
    | RunnablePassthrough.assign(critique=critique_chain)
    | refinement_chain
)
```

Plain loop (iterative, with cap and stop condition):

```python
for i in range(max_iterations):
    response = llm.invoke(message_history)      # generate, then refine
    current_code = response.content
    message_history.append(response)

    critique = llm.invoke(reflector_prompt).content
    if "CODE_IS_PERFECT" in critique:
        break
    message_history.append(HumanMessage(content=f"Critique: {critique}"))
```

Google ADK (Producer-Critic):

```python
review_pipeline = SequentialAgent(
    name="WriteAndReview_Pipeline",
    sub_agents=[generator, reviewer],   # output_key="draft_text" -> "review_output"
)
```

## Framework notes
- **LangChain / LangGraph** — LCEL expresses one reflection step via chained `RunnablePassthrough.assign`; true iteration needs a stateful graph (LangGraph) or an explicit Python loop.
- **Google ADK** — `SequentialAgent` runs producer then critic, passing the draft through `session.state` keys set by each agent's `output_key`.

## Failure modes in depth
- **Non-convergence** — the critic always finds something, so the loop runs forever. Always pair a `max_iterations` cap with an explicit stop sentinel, and return the best draft when the cap is reached.
- **Self-critique rubber-stamping** — the same model that wrote the draft shares its blind spots and approves its own errors. Use a separate critic agent with its own role prompt and rubric, or a tool-based oracle such as tests.
- **Context overflow** — appending every draft and critique to `message_history` grows the prompt each round until it is truncated or throttled. Keep only the latest draft plus the current critique, or summarize prior rounds.
- **Multiplied cost and latency** — each iteration costs a generate plus a critique call. Budget iterations up front and reserve reflection for outputs where quality outranks speed.

## Source
Chapter 4 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_04_Reflection_(ADK).ipynb, Chapter_04_Reflection_(Iterative_Loop).ipynb, Chapter_04_Reflection_(LangChain).ipynb.
