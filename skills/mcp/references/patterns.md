# MCP patterns (Ch 10)

Five notebooks: FastMCP server, FastMCP client agent, ADK FastMCP bridge, filesystem agent + init.

Server (`fastmcp_server.py`): `from fastmcp import FastMCP, tool`; `@tool()` greeting function; `pip install fastmcp`; run `python fastmcp_server.py`.

Client: `LlmAgent(model='gemini-2.0-flash', name='fastmcp_greeter_agent', instruction=...)` + `MCPToolset(HttpServerParameters(url='http://localhost:8000'))`.

Filesystem agent: `MCPToolset(StdioServerParameters(command='npx'|'python3', args=[...]))` with `TARGET_FOLDER_PATH` pinned to `mcp_managed_files/`; variants for Drive/Sheets via `StdioConnectionParams` env (`SERVICE_ACCOUNT_PATH`, `DRIVE_FOLDER_ID`).

Package layout: `agent.py` + `__init__.py` (`from . import agent`) per ADK sample convention.

## Notebook extracts (on-demand detail)

### Chapter_10_MCP_(ADK_FastMCP_Server).ipynb

```python
root_agent = LlmAgent(
instruction='You are a friendly assistant that can greet people by their name. Use the "greet" tool.',
MCPToolset(
# ./adk_agent_samples/fastmcp_client_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, HttpServerParameters
# Make sure your fastmcp_server.py (defined previously) is running on this port.
# Optional: Filter which tools from the MCP server are exposed
# For this example, we're expecting only 'greet'
import os
```

### Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb

```python
from . import agent
```

### Chapter_10_MCP_(FastMCP_Server_Example).ipynb

```python
def greet(name: str) -> str:
# This script demonstrates how to create a simple MCP server using FastMCP.
# It exposes a single tool that generates a greeting.
# 3. Run from your terminal: python fastmcp_server.py
from fastmcp import FastMCP, tool
# The `@tool()` decorator registers this Python function as an MCP tool.
# The docstring becomes the tool's description for the LLM.
# By default, FastMCP runs on http://localhost:8000
# and automatically discovers functions decorated with @tool().
# For a simple script, `run()` is sufficient.
```

### Chapter_10_MCP_(Filesystem_Example_agent).ipynb

```python
root_agent = LlmAgent(
instruction=(
MCPToolset(
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
# Create a reliable absolute path to a folder named 'mcp_managed_files'
# within the same directory as this agent script.
# This ensures the agent works out-of-the-box for demonstration.
# For production, you would point this to a more persistent and secure location.
# Ensure the target directory exists before the agent needs it.
```

### Chapter_10_MCP_(Filesystem_Example_init).ipynb

```python
from . import agent
```
