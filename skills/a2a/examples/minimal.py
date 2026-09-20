"""Chapter 15 — A2A Agent Card (discovery surface for peer agents)."""
from a2a import AgentCard, AgentCapabilities, AgentSkill  # illustrative imports

def calendar_card(host: str, port: int) -> AgentCard:
    return AgentCard(
        name="Calendar Agent",
        url=f"http://{host}:{port}/",
        capabilities=AgentCapabilities(streaming=True),
        skills=[AgentSkill(id="check_availability", name="Check Availability")],
    )
