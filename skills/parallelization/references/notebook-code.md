# Parallelization — reference patterns

Source: Chapter 3 + `Chapter_03_Parallelization_(Google_ADK).ipynb`,
`Chapter_03_Parallelization_(LangChain).ipynb`.

## Rule of thumb (book)
Use when a workflow contains multiple independent operations that can run
simultaneously: fetching from several APIs, processing chunks, generating
several pieces of content for later synthesis. The book warns that
concurrency adds real complexity to design, debugging and logging.

## Pattern A: LangChain `RunnableParallel` + synthesis
```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

summarize_chain = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following topic concisely:"), ("user", "{topic}")]) | llm | StrOutputParser()
questions_chain = ChatPromptTemplate.from_messages([
    ("system", "Generate three interesting questions about the following topic:"), ("user", "{topic}")]) | llm | StrOutputParser()
terms_chain = ChatPromptTemplate.from_messages([
    ("system", "Identify 5-10 key terms from the following topic, separated by commas:"), ("user", "{topic}")]) | llm | StrOutputParser()

map_chain = RunnableParallel({
    "summary": summarize_chain,
    "questions": questions_chain,
    "key_terms": terms_chain,
    "topic": RunnablePassthrough(),     # keep the original input for the synthesiser
})

synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", """Based on the following information:
     Summary: {summary}
     Related Questions: {questions}
     Key Terms: {key_terms}
     Synthesize a comprehensive answer."""),
    ("user", "Original topic: {topic}")])

full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()
response = await full_parallel_chain.ainvoke("The history of space exploration")
```
- The single string input is broadcast to every runnable in the map.
- Use `ainvoke` so branches actually overlap on I/O.

## Pattern B: ADK `ParallelAgent` inside a `SequentialAgent`
```python
researcher_agent_1 = LlmAgent(name="RenewableEnergyResearcher", model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    tools=[google_search], output_key="renewable_energy_result")
# researcher_agent_2 -> output_key="ev_technology_result"
# researcher_agent_3 -> output_key="carbon_capture_result"

parallel_research_agent = ParallelAgent(name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3])

merger_agent = LlmAgent(name="SynthesisAgent", model=GEMINI_MODEL, instruction="""...
**Crucially: Your entire response MUST be grounded *exclusively* on the information provided
in the 'Input Summaries' below. Do NOT add any external knowledge.**

**Input Summaries:**
*   **Renewable Energy:** {renewable_energy_result}
*   **Electric Vehicles:** {ev_technology_result}
*   **Carbon Capture:** {carbon_capture_result}

**Output Format:**
## Summary of Recent Sustainable Technology Advancements
### Renewable Energy Findings
### Electric Vehicle Findings
### Carbon Capture Findings
### Overall Conclusion
Output *only* the structured report following this format.""")

root_agent = SequentialAgent(name="ResearchAndSynthesisPipeline",
    sub_agents=[parallel_research_agent, merger_agent])
```
Mechanics:
- Each parallel branch writes to session state via `output_key`.
- `{state_key}` placeholders in the merger's instruction are filled from state.
- `ParallelAgent` completes only when every sub-agent has finished (join).

## Synthesis prompt guidance
Tell the merger explicitly to (1) attribute each finding to its branch,
(2) use only the provided inputs, (3) follow a fixed output skeleton. Without
(2) the merger will pad with training knowledge.

## Operational concerns
- Fan-out N calls hits provider rate limits; add a semaphore or batch size.
- Partial failure: decide per-branch whether to fail the join or substitute
  a placeholder ("no result") and flag it for the synthesiser.
- Trace/log each branch with its key; interleaved logs are unreadable otherwise.
- ADK can also parallelise via LLM-driven delegation from a coordinator; explicit
  `ParallelAgent` is more predictable.

## Combine with
`prompt-chaining` (sequential before/after the fan-out), `routing` (decide
which branches to run), `multi-agent` (branches are specialists).
