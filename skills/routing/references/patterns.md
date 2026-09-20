# Routing — Pattern reference

Load this file only when implementing `routing`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when the agent must choose among workflows, tools, or sub-agents from user input or current state (triage).

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Router pattern, using an LLM as a Router.

## Notebooks (extracted)

Routing

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

## Failure modes (skill-level)
- Misclassification sends work to the wrong specialist
- Missing default/unclear bucket drops queries
- LLM router verbose output breaks exact-match branches

## Chains with
`prompt-chaining`, `tool-use`
