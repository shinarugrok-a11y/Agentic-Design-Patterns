"""Chapter 12 — Primary tool, then fallback if state flag is set."""
from google.adk.agents import SequentialAgent

def robust_location_agent(primary, fallback, responder):
    return SequentialAgent(
        name="robust_location_agent",
        sub_agents=[primary, fallback, responder],
    )
# fallback instruction:
# if state["primary_location_failed"]: extract city; call get_general_area_info
