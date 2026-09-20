"""Chapter 5 — Tool-calling agent (LangChain). Swap search_information for a real API."""
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

@tool
def search_information(query: str) -> str:
    """Provides factual information on a given topic."""
    known = {"capital of france": "Paris"}
    return known.get(query.lower(), "No info found.")

def build_executor(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, [search_information], prompt)
    return AgentExecutor(agent=agent, tools=[search_information], verbose=True)
