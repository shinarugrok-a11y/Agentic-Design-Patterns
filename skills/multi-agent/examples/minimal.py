"""Chapter 7 — Sequential multi-agent handoff via output_key."""
from google.adk.agents import SequentialAgent, Agent

def pipeline():
    fetch = Agent(name="Step1_Fetch", output_key="data",
                  instruction="Fetch or draft the raw material.")
    process = Agent(name="Step2_Process",
                    instruction="Analyze state['data'] and produce the final answer.")
    return SequentialAgent(name="MyPipeline", sub_agents=[fetch, process])
