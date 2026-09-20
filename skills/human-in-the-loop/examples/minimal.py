"""Chapter 13 — Escalate to a human; inject personalization via callback."""
from google.genai import types

def personalization_callback(callback_context, llm_request):
    info = callback_context.state.get("customer_info", {})
    note = f"Customer Name: {info.get('name')}; Tier: {info.get('tier')}"
    llm_request.contents.insert(
        0, types.Content(role="system", parts=[types.Part(text=note)])
    )
    return None  # required so the modified request proceeds

def escalate_to_human(issue: str, context: dict) -> str:
    """Pause for a specialist. Do not continue irreversible work."""
    return f"ESCALATED: {issue}"
