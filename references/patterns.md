# Agentic Design Patterns — Notebook Pattern Reference

Extracted from `/workspace/chapter_notebooks` (Chapters 1–21). Appendices excluded.

> **Note:** None of the chapter notebooks contain markdown cells; caveats and context live in code comments, docstrings, and inline prompt text.

---

## Chapter 1: Prompt Chaining

### Notebooks
- `Chapter_01_Prompt_Chaining_(Code_Example).ipynb`
- `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`

### Patterns
- **Framework:** LangChain LCEL (`ChatPromptTemplate | llm | StrOutputParser`)
- **Two-stage chain:** extract specs → transform to JSON via dict passthrough
- **Intermediate binding:** `{"specifications": extraction_chain}` feeds prior output into next prompt
- **JSON example notebook:** sample structured output (not executable Python)

### Prompt templates
```
Extract the technical specifications from the following text:

{text_input}
```
```
Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:

{specifications}
```

### Minimal code
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)

prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with "
    "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

result = full_chain.invoke({"text_input": "3.5 GHz octa-core, 16GB RAM, 1TB NVMe SSD."})
```

### Caveats
- Requires `OPENAI_API_KEY` (optionally via `.env` / `dotenv`)
- `JSON_Example` notebook is reference output only — not runnable code
- Use `temperature=0` for deterministic structured extraction

---

## Chapter 2: Routing

### Notebooks
- `Chapter_02_Routing_(Google_ADK).ipynb`
- `Chapter_02_Routing_(LangGraph).ipynb`
- `Chapter_02_Routing_(Openrouter).ipynb`

### Patterns
- **Google ADK:** coordinator `Agent` with `sub_agents` → LLM-driven Auto-Flow delegation; specialists use `FunctionTool`
- **LangGraph/LCEL:** `RunnableBranch` routes on LLM classifier output (`booker` / `info` / `unclear`)
- **OpenRouter:** raw REST API to multi-model gateway (no agent framework)
- **Execution:** ADK uses `InMemoryRunner`, session per request, `event.is_final_response()`

### Prompt templates
Coordinator instruction (ADK):
```
You are the main coordinator. Your only task is to analyze incoming user requests
and delegate them to the appropriate specialist agent. Do not try to answer the user directly.
- For any requests related to booking flights or hotels, delegate to the 'Booker' agent.
- For all other general information questions, delegate to the 'Info' agent.
```

Router system prompt (LangGraph):
```
Analyze the user's request and determine which specialist handler should process it.
 - If the request is related to booking flights or hotels, output 'booker'.
 - For all other general information questions, output 'info'.
 - If the request is unclear or doesn't fit either category, output 'unclear'.
 ONLY output one word: 'booker', 'info', or 'unclear'.
```

### Minimal code
```python
# LangGraph-style routing
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

router = ChatPromptTemplate.from_messages([
    ("system", "Output ONLY: 'booker', 'info', or 'unclear'."),
    ("user", "{request}")
]) | llm | StrOutputParser()

branch = RunnableBranch(
    (lambda x: x["decision"].strip() == "booker",
     RunnablePassthrough.assign(output=lambda x: booking_handler(x["request"]))),
    (lambda x: x["decision"].strip() == "info",
     RunnablePassthrough.assign(output=lambda x: info_handler(x["request"]))),
    RunnablePassthrough.assign(output=lambda x: unclear_handler(x["request"])),
)
chain = {"decision": router, "request": RunnablePassthrough()} | branch
```

### Caveats
- ADK requires Google ADK installed and authenticated
- LangGraph example needs `GOOGLE_API_KEY` for `ChatGoogleGenerativeAI`
- OpenRouter snippet is incomplete (placeholder API key, no response handling)
- ADK: iterate `event.content.parts` carefully — prefer `event.content.text` when available

---

## Chapter 3: Parallelization

### Notebooks
- `Chapter_03_Parallelization_(Google_ADK).ipynb`
- `Chapter_03_Parallelization_(LangChain).ipynb`

### Patterns
- **ADK:** `ParallelAgent` runs sub-agents concurrently; each uses `output_key` → state; `SequentialAgent` chains parallel block then merger
- **LangChain:** `RunnableParallel` runs summarize / questions / terms chains; synthesis prompt merges results
- **Merger grounding:** synthesis agent must use only parallel outputs (no external knowledge)

### Prompt templates
Merger instruction (ADK) — key constraint:
```
**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**
```

LangChain synthesis system prompt:
```
Based on the following information:
 Summary: {summary}
 Related Questions: {questions}
 Key Terms: {key_terms}
 Synthesize a comprehensive answer.
```

### Minimal code
```python
# LangChain parallel + synthesis
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

map_chain = RunnableParallel(
    summary=summarize_chain,
    questions=questions_chain,
    key_terms=terms_chain,
    topic=RunnablePassthrough(),
)
full_chain = map_chain | synthesis_prompt | llm | StrOutputParser()
await full_chain.ainvoke("The history of space exploration")
```

```python
# ADK pattern (fragment)
parallel_research = ParallelAgent(name="ParallelWebResearchAgent", sub_agents=[r1, r2, r3])
pipeline = SequentialAgent(name="ResearchAndSynthesisPipeline", sub_agents=[parallel_research, merger_agent])
```

### Caveats
- ADK snippet is partial — requires full `agent.py` setup per ADK quickstart
- LangChain example uses `async`/`ainvoke`
- ADK researchers depend on `google_search` tool and `GEMINI_MODEL` constant defined elsewhere

---

## Chapter 4: Reflection

### Notebooks
- `Chapter_04_Reflection_(ADK).ipynb`
- `Chapter_04_Reflection_(Iterative_Loop).ipynb`
- `Chapter_04_Reflection_(LangChain).ipynb`

### Patterns
- **ADK:** `SequentialAgent` — generator writes to `output_key="draft_text"`, reviewer reads state and outputs structured dict to `review_output`
- **Iterative loop:** generate → reflect → refine until `CODE_IS_PERFECT` or max iterations
- **LangChain:** LCEL pipeline: generate → critique → refine via `RunnablePassthrough.assign`

### Prompt templates
Fact-checker (ADK):
```
You are a meticulous fact-checker.
1. Read the text provided in the state key 'draft_text'.
2. Carefully verify the factual accuracy of all claims.
3. Your final output must be a dictionary containing two keys:
   - "status": A string, either "ACCURATE" or "INACCURATE".
   - "reasoning": A string providing a clear explanation for your status, citing specific issues if any are found.
```

Reflector (Iterative Loop):
```
You are a senior software engineer and an expert in Python.
Your role is to perform a meticulous code review.
Critically evaluate the provided Python code based on the original task requirements.
Look for bugs, style issues, missing edge cases, and areas for improvement.
If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
Otherwise, provide a bulleted list of your critiques.
```

### Minimal code
```python
# ADK write-and-review pipeline
from google.adk.agents import SequentialAgent, LlmAgent

generator = LlmAgent(name="DraftWriter", instruction="Write a short paragraph.", output_key="draft_text")
reviewer = LlmAgent(name="FactChecker", instruction="Review state['draft_text']...", output_key="review_output")
pipeline = SequentialAgent(name="WriteAndReview_Pipeline", sub_agents=[generator, reviewer])
```

```python
# LangChain single-pass reflection
full_reflection_chain = (
    RunnablePassthrough.assign(initial_description=generation_chain)
    | RunnablePassthrough.assign(critique=critique_chain)
    | refinement_chain
)
```

### Caveats
- Iterative loop requires `OPENAI_API_KEY`; uses `gpt-4o` at low temperature
- LangChain reflection is single-pass (not looped) unlike iterative example
- ADK reviewer expects structured dict output — validate parsing in production

---

## Chapter 5: Tool Use

### Notebooks
- `Chapter_05_Tool_Use_(CrewAI).ipynb`
- `Chapter_05_Tool_Use_(Executing_Code).ipynb`
- `Chapter_05_Tool_Use_(Google_Search).ipynb`
- `Chapter_05_Tool_Use_(LangChain).ipynb`
- `Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb`

### Patterns
- **CrewAI:** `@tool` decorator; tools return typed data or raise `ValueError` (not error strings)
- **ADK Google Search:** `Agent` + `google_search` tool + `Runner`/`InMemorySessionService`
- **ADK code execution:** `BuiltInCodeExecutor()` on `LlmAgent`; inspect `part.executable_code` and `part.code_execution_result`
- **LangChain:** `create_tool_calling_agent` + `AgentExecutor`; requires `{agent_scratchpad}` placeholder
- **Vertex AI:** `VSearchAgent` with `datastore_id`; streams via `run_async`

### Prompt templates
Calculator agent (ADK):
```
You are a calculator agent.
When given a mathematical expression, write and execute Python code to calculate the result.
Return only the final numerical result as plain text, without markdown or code blocks.
```

LangChain agent system:
```
You are a helpful assistant.
```

### Minimal code
```python
# LangChain tool-calling agent
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def search_information(query: str) -> str:
    """Provides factual information on a given topic."""
    return simulated_results.get(query.lower(), "No info found.")

agent = create_tool_calling_agent(llm, [search_information], agent_prompt)
executor = AgentExecutor(agent=agent, verbose=True)
await executor.ainvoke({"input": "What is the capital of France?"})
```

```python
# ADK with Google Search
root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash-exp",
    tools=[google_search],
    instruction="I can answer your questions by searching the internet.",
)
```

### Caveats
- CrewAI: raise exceptions from tools; let agent handle failures
- Vertex AI Search requires `DATASTORE_ID` env var and GCP permissions
- LangChain notebook has duplicate cells (pip install + getpass variants)
- Code executor: use `run_async` and check `event.is_final_response()` for final text
- `nest_asyncio.apply()` needed for async in Jupyter

---

## Chapter 6: Planning

### Notebooks
- `Chapter_06_Planning_(Code_Example).ipynb`
- `Chapter_06_Planning_(Deep_Research_API).ipynb`

### Patterns
- **CrewAI:** single agent, single task with two-step description (plan bullets → write summary); `Process.sequential`
- **OpenAI Deep Research:** `client.responses.create` with `o3-deep-research`, `web_search_preview` tool, reasoning summary
- **Structured output:** task `expected_output` defines `### Plan` and `### Summary` sections

### Prompt templates
Deep Research system message:
```
You are a professional researcher preparing a structured, data-driven report.
Focus on data-rich insights, use reliable sources, and include inline citations.
```

CrewAI task description pattern:
```
1. Create a bullet-point plan for a summary on the topic: '{topic}'.
2. Write the summary based on your plan, keeping it around 200 words.
```

### Minimal code
```python
# CrewAI plan-then-write
planner = Agent(role='Article Planner and Writer', goal='Plan and write a concise summary.', llm=llm)
task = Task(
    description="1. Create a bullet-point plan...\n2. Write the summary...",
    expected_output="### Plan\n...\n### Summary\n...",
    agent=planner,
)
result = Crew(agents=[planner], tasks=[task], process=Process.sequential).kickoff()
```

```python
# OpenAI Deep Research (fragment)
response = client.responses.create(
    model="o3-deep-research-2025-06-26",
    input=[{"role": "developer", "content": [{"type": "input_text", "text": system_message}]},
           {"role": "user", "content": [{"type": "input_text", "text": user_query}]}],
    reasoning={"summary": "auto"},
    tools=[{"type": "web_search_preview"}],
)
```

### Caveats
- Deep Research requires OpenAI API access to research models
- Inspect `response.output` for reasoning, web_search_call, code_interpreter_call steps
- CrewAI uses `gpt-4-turbo` — assign explicit `llm` to agent

---

## Chapter 7: Multi-Agent Collaboration

### Notebooks
- `Chapter_07_Multi_Agent_(ADK_Gemini_AgentTool).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Loop).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Parallel).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb`
- `Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb`

### Patterns
- **SequentialAgent:** ordered sub-agents; `output_key` passes state between steps
- **ParallelAgent:** concurrent sub-agents writing to distinct state keys
- **LoopAgent:** `max_iterations` + custom `BaseAgent` that `EventActions(escalate=True)` to break
- **AgentTool:** wrap `LlmAgent` as tool; parent calls via `input` parameter
- **Custom BaseAgent:** extend `_run_async_impl` → `AsyncGenerator[Event]`
- **CrewAI:** researcher → writer with `context=[research_task]`; `Process.sequential`

### Prompt templates
ImageGen specialist:
```
You are an image generation specialist. Your task is to take the user's request
and use the `generate_image` tool to create the image.
The user's entire request should be used as the 'prompt' argument for the tool.
After the tool returns the image bytes, you MUST output the image.
```

Coordinator delegation:
```
When asked to greet, delegate to the Greeter. When asked to perform a task, delegate to the TaskExecutor.
```

### Minimal code
```python
# Sequential pipeline
step1 = Agent(name="Step1_Fetch", output_key="data")
step2 = Agent(name="Step2_Process", instruction="Analyze state['data']...")
pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])
```

```python
# Agent-as-tool
image_tool = agent_tool.AgentTool(agent=image_generator_agent, description="Generate an image from a prompt.")
artist = LlmAgent(name="Artist", tools=[image_tool], instruction="Invent a prompt, then call ImageGen.")
```

```python
# CrewAI multi-agent
writing_task = Task(description="Write 500-word blog...", agent=writer, context=[research_task])
Crew(agents=[researcher, writer], tasks=[research_task, writing_task], process=Process.sequential, llm=llm).kickoff()
```

### Caveats
- `Sequential` notebook is minimal (~699 chars) — omits model/instruction on step1
- Loop agent: `ConditionChecker` must read `context.session.state`
- Parallel example has commented-out Runner invocation
- CrewAI requires `GOOGLE_API_KEY` for Gemini

---

## Chapter 8: Memory Management

### Notebooks
- `Chapter_08_Memory_(ADK_Explicit_State_Update).ipynb`
- `Chapter_08_Memory_(ADK_LlmAgent_output_key).ipynb`
- `Chapter_08_Memory_(ADK_MemoryService_InMemory).ipynb`
- `Chapter_08_Memory_(ADK_SessionService).ipynb`
- `Chapter_08_Memory_(LangChain_LangGraph).ipynb`

### Patterns
- **ADK state via tools:** `ToolContext.state` for namespaced keys (`user:`, `temp:`)
- **output_key:** agent response auto-persisted to session state
- **Session services:** `InMemorySessionService`, `DatabaseSessionService`, `VertexAiSessionService`
- **Memory services:** `InMemoryMemoryService`, `VertexAiRagMemoryService`
- **LangChain:** `ConversationBufferMemory`, `ChatMessageHistory`, `LLMChain` with `{history}` / `MessagesPlaceholder`
- **LangGraph store:** `InMemoryStore` with embed/search/filter namespaces

### Prompt templates
LangChain travel agent template:
```
You are a helpful travel agent.

Previous conversation:
{history}

New question: {question}
Response:
```

### Minimal code
```python
# ADK output_key persistence
greeting_agent = LlmAgent(name="Greeter", instruction="Generate a short greeting.", output_key="last_greeting")
# After runner.run(...): session.state["last_greeting"] is populated
```

```python
# Tool-based state update
def log_user_login(tool_context: ToolContext) -> dict:
    state = tool_context.state
    state["user:login_count"] = state.get("user:login_count", 0) + 1
    return {"status": "success"}
```

```python
# LangGraph memory store
store = InMemoryStore(index={"embed": embed, "dims": 2})
store.put(("user_id", "app"), "a-memory", {"rules": ["User likes short language"]})
items = store.search(("user_id", "app"), query="language preferences")
```

### Caveats
- `InMemory*` services lose data on restart
- Vertex services need GCP project, corpus/engine IDs, `google-adk[vertexai]`
- Database session needs SQLAlchemy driver (e.g. `psycopg2`)
- LangChain `return_messages=True` required for chat models with `MessagesPlaceholder`
- Check state *after* runner finishes all events

---

## Chapter 9: Learning and Adaptation

### Notebooks
- `Chapter_09_Adaptation_(OpenEvolve).ipynb`

### Patterns
- **OpenEvolve:** evolutionary program improvement via `initial_program_path`, `evaluation_file`, `config_path`
- **Async execution:** `await evolve.run(iterations=N)` returns best program with metrics

### Prompt templates
None in notebook.

### Minimal code
```python
from openevolve import OpenEvolve

evolve = OpenEvolve(
    initial_program_path="path/to/initial_program.py",
    evaluation_file="path/to/evaluator.py",
    config_path="path/to/config.yaml",
)
best_program = await evolve.run(iterations=1000)
print(best_program.metrics)
```

### Caveats
- **Thin notebook** — stub only; requires external program, evaluator, and config files
- Async context required (`await`)
- No markdown documentation in notebook

---

## Chapter 10: Model Context Protocol (MCP)

### Notebooks
- `Chapter_10_MCP_(ADK_FastMCP_Server).ipynb` *(filename says Server; content is ADK client)*
- `Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb` ⚠️ thin
- `Chapter_10_MCP_(FastMCP_Server_Example).ipynb`
- `Chapter_10_MCP_(Filesystem_Example_agent).ipynb`
- `Chapter_10_MCP_(Filesystem_Example_init).ipynb` ⚠️ thin

### Patterns
- **FastMCP server:** `@tool()` decorator on functions; `FastMCP().run()` on localhost:8000
- **ADK client:** `MCPToolset(connection_params=HttpServerParameters(url=...), tool_filter=['greet'])`
- **Stdio MCP:** `StdioServerParameters(command='npx', args=["-y", "@modelcontextprotocol/server-filesystem", ABS_PATH])`
- **Package init:** `from . import agent` in `__init__.py`

### Prompt templates
FastMCP greeter agent instruction:
```
You are a friendly assistant that can greet people by their name. Use the "greet" tool.
```

Filesystem agent instruction:
```
Help the user manage their files. You can list files, read files, and write files.
You are operating in the following directory: {TARGET_FOLDER_PATH}
```

### Minimal code
```python
# FastMCP server
from fastmcp import FastMCP, tool

@tool()
def greet(name: str) -> str:
    """Generates a personalized greeting."""
    return f"Hello, {name}!"

FastMCP().run()  # http://localhost:8000
```

```python
# ADK MCP client
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, HttpServerParameters

agent = LlmAgent(
    model='gemini-2.0-flash',
    tools=[MCPToolset(connection_params=HttpServerParameters(url="http://localhost:8000"), tool_filter=['greet'])],
)
```

### Caveats
- Server must be running before client connects
- Filesystem MCP requires **absolute path** to allowed directory
- Init notebooks are one-line package stubs
- `Filesystem_Example_agent` second cell shows Google Sheets/Drive stdio configs (incomplete snippet)
- `pip install fastmcp` required for server

---

## Chapter 11: Goal Setting and Monitoring

### Notebooks
- `Chapter_11_Goal_Setting_(Iteration).ipynb`

### Patterns
- **Goal-driven iteration:** generate code → LLM feedback → LLM judge (`True`/`False`) → repeat up to `max_iterations`
- **Monitoring:** separate reviewer and binary goals-met classifier
- **Artifact output:** save `.py` with LLM-generated filename suffix
- **Framework:** LangChain `ChatOpenAI` (gpt-4o), no agent framework

### Prompt templates
Code generation:
```
You are an AI coding agent. Your job is to write Python code based on the following use case:

Use Case: {use_case}

Your goals are:
- {goal1}
- {goal2}

Please return only the revised Python code. Do not include comments or explanations outside the code.
```

Goals-met check:
```
Based on the feedback above, have the goals been met?

Respond with only one word: True or False.
```

### Minimal code
```python
for i in range(max_iterations):
    code = llm.invoke(generate_prompt(use_case, goals, previous_code, feedback)).content
    feedback = llm.invoke(get_code_feedback(code, goals)).content
    if goals_met(feedback, goals):
        break
    previous_code = clean_code_block(code)
save_code_to_file(add_comment_header(code, use_case), use_case)
```

### Caveats
- Requires `OPENAI_API_KEY`; docstring notes gpt-4o fallback options
- Max 5 iterations by default — may stop before goals truly met if judge is lenient
- Filename generated by LLM summary — may produce odd names
- First two cells are pip install / commented debug only

---

## Chapter 12: Exception Handling and Recovery

### Notebooks
- `Chapter_12_Exception_Handling_(Fallback).ipynb`

### Patterns
- **Sequential fallback chain:** primary handler → fallback (reads `state["primary_location_failed"]`) → response agent
- **State-driven recovery:** fallback agent inspects state flags set by failed primary tool
- **Separation of concerns:** response agent has no tools — only formats final state

### Prompt templates
Primary handler:
```
Your job is to get precise location information.
Use the get_precise_location_info tool with the user's provided address.
```

Fallback handler:
```
Check if the primary location lookup failed by looking at state["primary_location_failed"].
- If it is True, extract the city from the user's original query and use the get_general_area_info tool.
- If it is False, do nothing.
```

### Minimal code
```python
robust_location_agent = SequentialAgent(
    name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent],
)
```

### Caveats
- **Incomplete snippet** — `get_precise_location_info` and `get_general_area_info` referenced but not defined in notebook
- Relies on primary tool setting `state["primary_location_failed"]` correctly
- ADK `gemini-2.0-flash-exp` model specified

---

## Chapter 13: Human-in-the-Loop

### Notebooks
- `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`

### Patterns
- **Escalation tool:** `escalate_to_human` for complex cases beyond automated troubleshooting
- **State-aware agent:** reads `state["customer_info"]["support_history"]` for personalization
- **Callback injection:** `personalization_callback` on `CallbackContext` inserts system message into `LlmRequest`
- **Workflow:** troubleshoot → create_ticket → escalate when needed

### Prompt templates
Technical support agent:
```
You are a technical support specialist for our electronics company.
FIRST, check if the user has a support history in state["customer_info"]["support_history"]. If they do, reference this history in your responses.
For technical issues:
1. Use the troubleshoot_issue tool to analyze the problem.
2. Guide the user through basic troubleshooting steps.
3. If the issue persists, use create_ticket to log the issue.
For complex issues beyond basic troubleshooting:
1. Use escalate_to_human to transfer to a human specialist.
Maintain a professional but empathetic tone.
```

Personalization callback injects:
```
IMPORTANT PERSONALIZATION:
Customer Name: {customer_name}
Customer Tier: {customer_tier}
Recent Purchases: ...
```

### Minimal code
```python
def personalization_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    info = callback_context.state.get("customer_info", {})
    note = f"\nIMPORTANT PERSONALIZATION:\nCustomer Name: {info.get('name')}\n..."
    llm_request.contents.insert(0, types.Content(role="system", parts=[types.Part(text=note)]))
    return None
```

### Caveats
- Tools are placeholders — replace with real ticketing/queue integrations
- Callback must return `None` to proceed with modified request
- No runnable demo loop in notebook — definition only

---

## Chapter 14: Knowledge Retrieval (RAG)

### Notebooks
- `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` ⚠️ thin
- `Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb`
- `Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb`

### Patterns
- **ADK Google Search:** minimal agent with search tool (search-augmented, not vector RAG)
- **LangChain + LangGraph:** load → chunk → embed (Weaviate) → retrieve node → generate node
- **Vertex AI RAG:** `VertexAiRagMemoryService` with corpus, `similarity_top_k`, `vector_distance_threshold`
- **Grounded generation:** "If you don't know the answer, just say that you don't know."

### Prompt templates
RAG QA template:
```
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:
```

### Minimal code
```python
# LangGraph RAG
workflow = StateGraph(RAGGraphState)
workflow.add_node("retrieve", retrieve_documents_node)
workflow.add_node("generate", generate_response_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
app = workflow.compile()
for s in app.stream({"question": "What did the president say about Justice Breyer"}):
    print(s)
```

```python
# ADK search agent (minimal)
search_agent = Agent(name="research_assistant", model="gemini-2.0-flash-exp",
                       instruction="Use the Google Search tool", tools=[Google Search])
```

### Caveats
- Google Search notebook is **very thin** (~284 chars) — 4 lines of code
- LangChain example downloads from GitHub URL (may get HTML not plain text)
- Weaviate embedded client + OpenAI embeddings required
- Vertex notebook is service setup only — no full agent loop
- Replace placeholder `RAG_CORPUS_RESOURCE_NAME`

---

## Chapter 15: Inter-Agent Communication (A2A)

### Notebooks
- `Chapter_15_Inter_Agent_(A2A).ipynb`
- `Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb` *(JSON schema, not Python)*
- `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` *(JSON-RPC examples)*

### Patterns
- **Agent Card:** metadata describing name, URL, capabilities, skills with examples
- **A2A server:** `AgentSkill` + `AgentCard` + `ADKAgentExecutor` + `A2AStarletteApplication` + uvicorn
- **Calendar agent:** `CalendarToolset` with OAuth; RFC3339 timestamps; `primary` calendar default
- **JSON-RPC:** `sendTask` (sync) vs `sendTaskSubscribe` (streaming)

### Prompt templates
Calendar agent instruction:
```
You are an agent that can help manage a user's calendar.

Users will request information about the state of their calendar or to make changes to
their calendar. Use the provided tools for interacting with the calendar API.

If not specified, assume the calendar the user wants is the 'primary' calendar.

When using the Calendar API tools, use well-formed RFC3339 timestamps.

Today is {datetime.datetime.now()}.
```

### Minimal code
```python
# A2A server setup (fragment)
agent_card = AgentCard(
    name='Calendar Agent',
    url=f'http://{host}:{port}/',
    capabilities=AgentCapabilities(streaming=True),
    skills=[AgentSkill(id='check_availability', name='Check Availability', ...)],
)
runner = Runner(app_name=agent_card.name, agent=adk_agent, ...)
a2a_app = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
uvicorn.run(Starlette(routes=a2a_app.routes()), host=host, port=port)
```

### Caveats
- Requires `GOOGLE_API_KEY` or `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
- OAuth env vars: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- WeatherBot and Sync_Streaming notebooks are **JSON reference docs**, not executable Python
- A2A notebook code is fragmented across two cells — imports missing in snippet

---

## Chapter 16: Resource-Aware Optimization

### Notebooks
- `Chapter_16_Resource_Optimization_(Code_Snippets).ipynb` *(conceptual, not runnable)*
- `Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb`

### Patterns
- **Model tiering:** `gemini-2.5-pro` for complex vs `gemini-2.5-flash` for simple
- **Query router:** custom `BaseAgent` routes by query length threshold
- **Classifier → model routing:** classify as `simple` / `reasoning` / `internet_search` → pick model + optional Google CSE
- **Model mapping:** simple→`gpt-4o-mini`, reasoning→`o4-mini`, search→`gpt-4o` with injected context

### Prompt templates
Classifier system message:
```
You are a classifier that analyzes user prompts and returns one of three categories ONLY:

- simple
- reasoning
- internet_search

Rules:
- Use 'simple' for direct factual questions that need no reasoning or current events.
- Use 'reasoning' for logic, math, or multi-step inference questions.
- Use 'internet_search' if the prompt refers to current events, recent data, or things not in your training data.

Respond ONLY with JSON like:
{ "classification": "simple" }
```

Critic agent (conceptual):
```
You are the **Critic Agent**, serving as the quality assurance arm of our collaborative research assistant system...
All criticism must be constructive. Your goal is to fortify the research, not invalidate it.
```

### Minimal code
```python
def handle_prompt(prompt: str) -> dict:
    classification = classify_prompt(prompt)["classification"]
    search_results = google_search(prompt) if classification == "internet_search" else None
    answer, model = generate_response(prompt, classification, search_results)
    return {"classification": classification, "response": answer, "model": model}
```

### Caveats
- Code_Snippets explicitly marked **"Conceptual Python-like structure, not runnable code"**
- OI example needs `OPENAI_API_KEY`, `GOOGLE_CUSTOM_SEARCH_API_KEY`, `GOOGLE_CSE_ID`
- Word-count routing is a toy heuristic — not production-ready
- Classifier uses `temperature=1` — may add variance

---

## Chapter 17: Reasoning Techniques

### Notebooks
- `Chapter_17_Reasoning_(CoT_Prompt).ipynb` *(prompt text + worked example, not Python)*
- `Chapter_17_Reasoning_(Executing_Code).ipynb`
- `Chapter_17_Reasoning_(Google_DeepSearch).ipynb` *(LangGraph fragment)*
- `Chapter_17_Reasoning_(Self_Correction).ipynb` *(prompt text + worked example)*

### Patterns
- **CoT prompt engineering:** 5-step process (analyze → search queries → simulate retrieval → synthesize → review)
- **Self-correction prompt:** compare output to requirements → identify weaknesses → propose fixes → rewrite
- **Multi-agent reasoning:** root agent with `AgentTool` wrapping search + code execution specialists
- **DeepSearch graph:** cyclic web_research ↔ reflection until ready to finalize

### Prompt templates
CoT agent opener:
```
You are an Information Retrieval Agent. Your goal is to answer the user's question comprehensively and accurately by thinking step-by-step.

Here's the process you must follow:

1.  **Analyze the Query:** Understand the core subject and specific requirements of the user's question.
2.  **Formulate Search Queries (for Knowledge Base):** Based on your analysis, generate a list of precise search queries...
3.  **Simulate Information Retrieval (Self-Correction/Reasoning):** For each search query, mentally consider what kind of information you expect to find.
4.  **Synthesize Information:** Based on the simulated retrieval... synthesize the gathered information into a coherent and complete answer.
5.  **Review and Refine:** Before finalizing, critically evaluate your answer.
```

Self-correction opener:
```
You are a highly critical and detail-oriented Self-Correction Agent. Your task is to review a previously generated piece of content against its original requirements and identify areas for improvement.
...
5.  **Generate Revised Content:** Based on your proposed improvements, rewrite the original content...
```

### Minimal code
```python
# Multi-agent reasoning (ADK)
search_agent = Agent(name='SearchAgent', tools=[google_search], instruction="You're a specialist in Google Search")
coding_agent = Agent(name='CodeAgent', code_executor=[BuiltInCodeExecutor], instruction="You're a specialist in Code Execution")
root_agent = Agent(
    name="RootAgent",
    tools=[agent_tool.AgentTool(agent=search_agent), agent_tool.AgentTool(agent=coding_agent)],
)
```

```python
# DeepSearch graph (fragment)
builder.add_conditional_edges("generate_query", continue_to_web_research, ["web_research"])
builder.add_conditional_edges("reflection", evaluate_research, ["web_research", "finalize_answer"])
graph = builder.compile(name="pro-search-agent")
```

### Caveats
- CoT and Self_Correction notebooks are **prompt documents** with worked examples — not executable Python
- DeepSearch notebook is graph wiring only — node functions not included
- Executing_Code notebook uses `code_executor=[BuiltInCodeExecutor]` (list form) — verify against current ADK API

---

## Chapter 18: Guardrails / Safety Patterns

### Notebooks
- `Chapter_18_Guardrails_(ADK_Validate_Tool).ipynb`
- `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` *(prompt text)*
- `Chapter_18_Guardrails_(Practical_Examples).ipynb`

### Patterns
- **before_tool_callback:** validate args against session state before tool execution; return error dict to block
- **LLM-as-guardrail:** pre-screen inputs; output JSON `{decision, reasoning}` or `{compliance_status, ...}`
- **CrewAI guardrails:** `Task(guardrail=validate_fn, output_pydantic=PolicyEvaluation)` with Pydantic validation
- **Default to safe/compliant** when ambiguous (explicit in prompts)

### Prompt templates
LLM guardrail decision protocol:
```
1.  Analyze the "Input to AI Agent" against **all** the "Guidelines for Unsafe Inputs."
2.  If the input clearly violates **any** of the guidelines, your decision is "unsafe."
3.  If you are genuinely unsure whether an input is unsafe (i.e., it's ambiguous or borderline), err on the side of caution and decide "safe."
```

CrewAI SAFETY_GUARDRAIL_PROMPT opening:
```
You are an AI Content Policy Enforcer, tasked with rigorously screening inputs intended for a primary AI system. Your core duty is to ensure that only content adhering to strict safety and relevance policies is processed.
```

Output format:
```json
{
 "compliance_status": "compliant" | "non-compliant",
 "evaluation_summary": "...",
 "triggered_policies": ["..."]
}
```

### Minimal code
```python
# ADK before_tool_callback
def validate_tool_params(tool, args, tool_context) -> Optional[Dict]:
    if args.get("user_id_param") != tool_context.state.get("session_user_id"):
        return {"status": "error", "error_message": "Tool call blocked: User ID validation failed."}
    return None  # allow execution

root_agent = Agent(..., before_tool_callback=validate_tool_params)
```

```python
# CrewAI guardrail task
evaluate_input_task = Task(
    description=f"{SAFETY_GUARDRAIL_PROMPT}\n\nUser Input: '{{user_input}}'",
    agent=policy_enforcer_agent,
    guardrail=validate_policy_evaluation,
    output_pydantic=PolicyEvaluation,
)
```

### Caveats
- Replace placeholder brand/competitor lists in prompts
- Practical Examples requires `GOOGLE_API_KEY` for Gemini Flash guardrail
- Guardrail defaulting to "compliant"/"safe" on ambiguity may allow borderline unsafe inputs
- `before_tool_callback` signature uses `ToolContext`, not `CallbackContext`

---

## Chapter 19: Evaluation and Monitoring

### Notebooks
- `Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb`
- `Chapter_19_Evaluation_(LLM_as_Judge).ipynb`

### Patterns
- **Exact-match accuracy:** strip/lowercase comparison (baseline metric)
- **Latency monitoring:** `time.perf_counter()` wrapper around agent/tool calls
- **Token tracking:** placeholder word-count monitor (replace with real tokenizer)
- **LLM-as-judge:** rubric-based evaluation with `response_mime_type="application/json"`
- **Domain rubric:** 5 criteria × 1–5 for legal survey questions

### Prompt templates
Legal survey rubric (excerpt):
```
You are an expert legal survey methodologist and a critical legal reviewer. Your task is to evaluate the quality of a given legal survey question.

Provide a score from 1 to 5 for overall quality, along with a detailed rationale and specific feedback.
Focus on the following criteria:

1.  **Clarity & Precision (Score 1-5):**
...
5.  **Appropriateness for Audience (Score 1-5):**

**Output Format:**
Your response MUST be a JSON object with the following keys:
* `overall_score`, `rationale`, `detailed_feedback`, `concerns`, `recommended_action`
```

### Minimal code
```python
def evaluate_response_accuracy(agent_output: str, expected_output: str) -> float:
    return 1.0 if agent_output.strip().lower() == expected_output.strip().lower() else 0.0

def timed_agent_action(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, (time.perf_counter() - start) * 1000
```

```python
# LLM judge
response = model.generate_content(
    full_prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.2, response_mime_type="application/json"
    ),
)
return json.loads(response.text)
```

### Caveats
- Exact-match fails on paraphrased correct answers
- Token monitor uses `len(text.split())` — not real token counts
- LLM judge: empty `response.parts` may indicate safety block — check `prompt_feedback.safety_ratings`
- Requires `GOOGLE_API_KEY` for Gemini judge

---

## Chapter 20: Prioritization

### Notebooks
- `Chapter_20_Prioritization_(SuperSimplePM).ipynb`

### Patterns
- **In-memory task manager:** Pydantic `Task` model; dict for O(1) lookup; `model_copy(update=...)`
- **Priority levels:** P0 (urgent/ASAP/critical), P1 (default), P2
- **ReAct PM agent:** `create_react_agent` + tools with `args_schema` (Pydantic)
- **Workflow:** create task first → assign priority/worker → list_all_tasks
- **Default assignment:** agent fills missing priority/assignee with P1 / Worker A

### Prompt templates
PM system prompt:
```
You are a focused Project Manager LLM agent. Your goal is to manage project tasks efficiently.

When you receive a new task request, follow these steps:
1.  First, create the task with the given description using the `create_new_task` tool. You must do this first to get a `task_id`.
2.  Next, analyze the user's request to see if a priority or an assignee is mentioned.
    - If a priority is mentioned (e.g., "urgent", "ASAP", "critical"), map it to P0. Use `assign_priority_to_task`.
    - If a worker is mentioned, use `assign_task_to_worker`.
3.  If any information (priority, assignee) is missing, you must make a reasonable default assignment (e.g., assign P1 priority and assign to 'Worker A').
4.  Once the task is fully processed, use `list_all_tasks` to show the final state.

Available workers: 'Worker A', 'Worker B', 'Review Team'
Priority levels: P0 (highest), P1 (medium), P2 (lowest)
```

### Minimal code
```python
class SuperSimpleTaskManager:
    def create_task(self, description: str) -> Task:
        task_id = f"TASK-{self.next_task_id:03d}"
        self.tasks[task_id] = Task(id=task_id, description=description)
        return self.tasks[task_id]

pm_agent_executor = AgentExecutor(
    agent=create_react_agent(llm, pm_tools, pm_prompt_template),
    tools=pm_tools,
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
    handle_parsing_errors=True,
)
await pm_agent_executor.ainvoke({"input": "Create urgent login task for Worker B"})
```

### Caveats
- In-memory only — no persistence across restarts
- Requires `OPENAI_API_KEY` via `.env`
- Urgency→P0 mapping is agent-interpreted, not rule-based
- `handle_parsing_errors=True` masks ReAct format failures

---

## Chapter 21: Exploration and Discovery

### Notebooks
- `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb`

### Patterns
- **Agent Laboratory pattern:** multi-role research pipeline (Postdoc, Professor, Reviewers)
- **Multi-reviewer scoring:** 3 independent reviewer personas → structured JSON review
- **Phased agents:** `self.phases` lists workflow stages; `context(phase)` builds state-specific prompts
- **Review template:** THOUGHT + REVIEW JSON with Originality/Quality/Clarity/Significance/Decision fields
- **Human-in-loop analogue:** iterative review/refinement before publication

### Prompt templates
Reviewer personas:
```
You are a harsh but fair reviewer and expect good experiments that lead to insights for the research topic.
```
```
You are a harsh and critical but fair reviewer who is looking for an idea that would be impactful in the field.
```
```
You are a harsh but fair open-minded reviewer that is looking for novel ideas that have not been proposed before.
```

Review JSON template (excerpt):
```
Respond in the following format:

THOUGHT:
<THOUGHT>

REVIEW JSON:
```json
<JSON>
```

In <JSON>, provide the review in JSON format with the following fields in the order:
- "Summary", "Strengths", "Weaknesses", "Originality", "Quality", "Clarity", "Significance"
- "Questions", "Limitations", "Ethical Concerns", "Soundness", "Presentation", "Contribution"
- "Overall" (1-10), "Confidence" (1-5), "Decision" (Accept or Reject only)
```

Professor readme prompt:
```
You are {role_description}
Here is the written paper
{report}
Task instructions: Your goal is to integrate all of the knowledge, code, reports, and notes provided to you and generate a readme.md for a github repository.
```

### Minimal code
```python
class ReviewersAgent:
    def inference(self, plan, report):
        reviews = [
            get_score(plan, report, reviewer_type="You are a harsh but fair reviewer..."),
            get_score(plan, report, reviewer_type="You are a harsh and critical but fair reviewer..."),
            get_score(plan, report, reviewer_type="You are a harsh but fair open-minded reviewer..."),
        ]
        return "\n".join(reviews)
```

### Caveats
- **Fragment from AgentLaboratory** — missing imports (`BaseAgent`, `query_model`, `get_score` body incomplete)
- Second cell is **empty**
- Not runnable standalone; reference only from https://github.com/SamuelSchmidgall/AgentLaboratory
- `get_score` has `attempts=3` retry loop but exception handling abbreviated

---

## Thin / Empty Notebooks Summary

| Notebook | Issue |
|----------|-------|
| `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb` | Sample JSON output only |
| `Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb` | Minimal fragment (~699 chars) |
| `Chapter_09_Adaptation_(OpenEvolve).ipynb` | 6-line stub, no supporting files |
| `Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb` | 1-line `__init__.py` |
| `Chapter_10_MCP_(Filesystem_Example_init).ipynb` | 1-line `__init__.py` |
| `Chapter_12_Exception_Handling_(Fallback).ipynb` | Missing tool function definitions |
| `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` | 4-line minimal agent |
| `Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb` | JSON schema reference |
| `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` | JSON-RPC examples |
| `Chapter_16_Resource_Optimization_(Code_Snippets).ipynb` | Marked non-runnable |
| `Chapter_17_Reasoning_(CoT_Prompt).ipynb` | Prompt text, not Python |
| `Chapter_17_Reasoning_(Self_Correction).ipynb` | Prompt text, not Python |
| `Chapter_17_Reasoning_(Google_DeepSearch).ipynb` | Graph fragment only |
| `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` | Prompt text, not Python |
| `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb` | Incomplete fragment + empty cell |

---

## Cross-Chapter Framework Index

| Framework | Chapters |
|-----------|----------|
| **LangChain / LCEL** | 1, 3, 4, 5, 8, 11, 14, 20 |
| **Google ADK** | 2, 3, 4, 5, 7, 8, 10, 12, 13, 14, 16, 17, 18 |
| **LangGraph** | 2, 8, 14, 17 |
| **CrewAI** | 5, 6, 7, 18 |
| **OpenAI API** | 6, 11, 16, 19, 21 |
| **FastMCP / MCP** | 10 |
| **A2A Protocol** | 15 |
| **OpenEvolve** | 9 |
| **Vertex AI** | 5, 8, 14 |
