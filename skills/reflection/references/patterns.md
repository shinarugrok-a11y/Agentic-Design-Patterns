# Reflection — reference patterns

Source: Chapter 4 + `Chapter_04_Reflection_(Iterative_Loop).ipynb`,
`Chapter_04_Reflection_(LangChain).ipynb`, `Chapter_04_Reflection_(ADK).ipynb`.

## Key takeaways (book)
- Loop of execution -> evaluation/critique -> refinement.
- Producer-Critic split (separate agent or prompted role) is more objective
  than self-reflection and yields structured feedback.
- Costs: latency, tokens, context-window growth, API throttling.
- Full iterative reflection wants stateful orchestration (LangGraph/ADK
  loops); a single critique-refine step is expressible in plain LCEL.

## Pattern A: iterative loop with stop token (LangChain)
```python
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
task_prompt = """Create a Python function `calculate_factorial` that:
1. Accepts a single integer n. 2. Returns n!. 3. Has a clear docstring.
4. factorial(0) == 1. 5. Raises ValueError for negative input."""

message_history = [HumanMessage(content=task_prompt)]
for i in range(max_iterations := 3):
    if i > 0:
        message_history.append(HumanMessage(content="Please refine the code using the critiques provided."))
    response = llm.invoke(message_history)
    current_code = response.content
    message_history.append(response)

    reflector_prompt = [
        SystemMessage(content="""You are a senior software engineer and an expert in Python.
Your role is to perform a meticulous code review.
Critically evaluate the provided Python code based on the original task requirements.
Look for bugs, style issues, missing edge cases, and areas for improvement.
If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
Otherwise, provide a bulleted list of your critiques."""),
        HumanMessage(content=f"Original Task:\n{task_prompt}\n\nCode to Review:\n{current_code}")]
    critique = llm.invoke(reflector_prompt).content
    if "CODE_IS_PERFECT" in critique:
        break
    message_history.append(HumanMessage(content=f"Critique of the previous code:\n{critique}"))
```
Design points: explicit sentinel (`CODE_IS_PERFECT`), hard `max_iterations`,
critic gets the *original task* plus the artifact, history carries critiques.

## Pattern B: single generate-critique-refine pass (LCEL)
```python
generation_chain = ChatPromptTemplate.from_messages([
    ("system", "Write a short, simple product description for a new smart coffee mug."),
    ("user", "{product_details}")]) | llm | StrOutputParser()

critique_chain = ChatPromptTemplate.from_messages([
    ("system", "Critique the following product description based on clarity, conciseness, and appeal. Provide specific suggestions for improvement."),
    ("user", "Product Description to Critique:\n{initial_description}")]) | llm | StrOutputParser()

refinement_chain = ChatPromptTemplate.from_messages([
    ("system", """Based on the original product details and the following critique,
rewrite the product description to be more effective.
Original Product Details: {product_details}
Critique: {critique}
Refined Product Description:"""), ("user", "")]) | llm | StrOutputParser()

full_reflection_chain = (RunnablePassthrough.assign(initial_description=generation_chain)
                         | RunnablePassthrough.assign(critique=critique_chain)
                         | refinement_chain)
```
`RunnablePassthrough.assign` accumulates fields so each stage sees the
original input plus prior outputs.

## Pattern C: Producer-Critic with ADK `SequentialAgent`
```python
generator = LlmAgent(name="DraftWriter",
    instruction="Write a short, informative paragraph about the user's subject.",
    output_key="draft_text")
reviewer = LlmAgent(name="FactChecker", instruction="""
    You are a meticulous fact-checker.
    1. Read the text provided in the state key 'draft_text'.
    2. Carefully verify the factual accuracy of all claims.
    3. Your final output must be a dictionary containing two keys:
       - "status": "ACCURATE" or "INACCURATE".
       - "reasoning": a clear explanation citing specific issues if any.""",
    output_key="review_output")
review_pipeline = SequentialAgent(name="WriteAndReview_Pipeline", sub_agents=[generator, reviewer])
```
Add a refinement agent that reads `review_output` and `draft_text`, and wrap
in `LoopAgent` (see `multi-agent`) with an escalate-on-ACCURATE checker to iterate.

## Critic prompt template
```
You are a {domain} reviewer. Evaluate the ARTIFACT against the REQUIREMENTS.
Report: (a) requirement violations, (b) bugs/errors, (c) concrete fixes.
If everything is satisfied respond exactly: {SENTINEL}
REQUIREMENTS: {task}
ARTIFACT: {artifact}
```

## Guardrails for the loop
- Cap iterations (2-3 is usually enough).
- Detect non-progress: identical artifact twice -> stop.
- Trim history or summarise critiques to avoid context overflow.
- Prefer a different model (or temperature) for the critic to reduce shared bias.
