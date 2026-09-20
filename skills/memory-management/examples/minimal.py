"""Chapter 8 — Persist last turn into session state via output_key."""
from google.adk.agents import LlmAgent

def greeter():
    return LlmAgent(
        name="Greeter",
        instruction="Generate a short greeting.",
        output_key="last_greeting",
    )
# After runner.run(...), read session.state["last_greeting"].
