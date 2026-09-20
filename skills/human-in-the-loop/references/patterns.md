# Human-in-the-Loop patterns (Ch 13)

One notebook: ADK customer-support escalation flow.

Pattern: support `Agent` with tools `troubleshoot_issue(issue)` and `create_ticket(issue_type, ...)`; escalation via `ToolContext` state + `CallbackContext`/`LlmRequest` hooks (`from google.adk.callbacks import CallbackContext`). Agent attempts auto-fix, then creates a ticket and pauses for human instead of guessing.

Prompt templates: agent instruction defines the autonomy boundary (auto-fix list vs escalate list); handoff message must include summary, attempted steps, and suggested action.

Rules: never auto-execute outside the allow-list; every escalation carries full context so the human decides in one read.

## Notebook extracts (on-demand detail)

### Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb

```python
def troubleshoot_issue(issue: str) -> dict:
def create_ticket(issue_type: str, details: str) -> dict:
def escalate_to_human(issue_type: str) -> dict:
technical_support_agent = Agent(
instruction="""
def personalization_callback(
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.callbacks import CallbackContext
from google.adk.models.llm import LlmRequest
```
