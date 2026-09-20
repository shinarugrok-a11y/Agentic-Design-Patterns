"""Chapter 17 — Root reasoner with search + code specialist tools."""
from google.adk.agents import Agent
from google.adk.tools import agent_tool

def root_reasoner(search_agent, code_agent) -> Agent:
    return Agent(
        name="RootAgent",
        instruction="Delegate search vs code; think step-by-step before answering.",
        tools=[
            agent_tool.AgentTool(agent=search_agent),
            agent_tool.AgentTool(agent=code_agent),
        ],
    )
