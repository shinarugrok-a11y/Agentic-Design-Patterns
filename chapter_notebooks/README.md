# Agentic Design Patterns - Code Notebooks

## About
Code notebooks for the book **"Agentic Design Patterns"** by Antonio Gulli.
This directory holds 65 `.ipynb` files: 56 chapter notebooks and 9 appendix notebooks.
They are illustrative snippets collected with the book materials. They are not a pinned, tested application.

## What is in these files
- 56 chapter notebooks, one or more framework variants per chapter. The index below matches the filenames in this directory.
- 56 `Chapter_*.SKILL.md` companions. `tools/validate.py` checks that each one is a byte-for-byte copy of `skills/<id>/SKILL.md` for that chapter. They are generated duplicates of the skill library, not separate notebook documentation.
- 2 appendix notebooks that contain code or examples: `Appendix_C_(Code).ipynb`, `Appendix_Pydantic.ipynb`.
- 7 appendix notebooks that are download placeholders (Appendix A, B, C overview, D, E, F, and G). Each one tells the reader to fetch a file from a Google Drive folder and replace the placeholder. That step is historical acquisition context. It is not required to read the PDF, use `skills/`, or run `skills/*/examples/minimal.py`. The placeholder cell calls `print(f"Code for: {chapter_name}")` and raises `NameError` when executed, because `chapter_name` is undefined.

## Execution status (repository audit, 2026-09-23)
Running a notebook requires the third-party libraries that notebook imports, plus API credentials where the code reads them. This repository does not pin those libraries and does not ship a `.env` file.

Observed in this audit:
- `Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb` executes offline with the Python standard library and prints local evaluation lines (accuracy, simulated latency, token counts).
- `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb` is a JSON object, not a prompt-chaining program.
- Seven notebooks do not parse as Python: `Chapter_03_Parallelization_(Google_ADK).ipynb` (leading indent), `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` (`tools=[Google Search]`), `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` (JSON examples inside a code cell), `Chapter_17_Reasoning_(CoT_Prompt).ipynb` and `Chapter_17_Reasoning_(Self_Correction).ipynb` (prompt text), `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` (prompt text), `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb` (indented excerpt).
- Stored cell outputs in five notebooks record earlier failures (`NameError`, `AuthenticationError` on the placeholder `YOUR_OPENAI_API_KEY`, `ModuleNotFoundError`). Those outputs are historical execution traces.
- Several files are fragments (`__init__.py` one-liners, `path/to/` placeholders, top-level `await`).

Treat framework calls inside notebooks as examples from the book materials. The offline pattern stubs that this repository actually executes are `skills/*/examples/minimal.py`.

## Book Information
- **Title**: Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems
- **Author**: Antonio Gulli — [LinkedIn](https://www.linkedin.com/in/searchguy/)
- **Book page**: [Amazon, ISBN 3032014018](https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018/). Current retail status was not re-checked.
- **Charity**: The book text says all author royalties are donated to Save the Children.

## File Structure
Naming convention: `Chapter_XX_Topic_(Variant).ipynb`

Each chapter may have multiple notebooks for different framework implementations (Google ADK, LangChain, CrewAI, etc.).

## Notebooks

### Chapter 1: Prompt Chaining
- `Chapter_01_Prompt_Chaining_(Code_Example).ipynb`
- `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`

### Chapter 2: Routing
- `Chapter_02_Routing_(Google_ADK).ipynb`
- `Chapter_02_Routing_(LangGraph).ipynb`
- `Chapter_02_Routing_(Openrouter).ipynb`

### Chapter 3: Parallelization
- `Chapter_03_Parallelization_(Google_ADK).ipynb`
- `Chapter_03_Parallelization_(LangChain).ipynb`

### Chapter 4: Reflection
- `Chapter_04_Reflection_(ADK).ipynb`
- `Chapter_04_Reflection_(Iterative_Loop).ipynb`
- `Chapter_04_Reflection_(LangChain).ipynb`

### Chapter 5: Tool Use
- `Chapter_05_Tool_Use_(CrewAI).ipynb`
- `Chapter_05_Tool_Use_(Executing_Code).ipynb`
- `Chapter_05_Tool_Use_(Google_Search).ipynb`
- `Chapter_05_Tool_Use_(LangChain).ipynb`
- `Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb`

### Chapter 6: Planning
- `Chapter_06_Planning_(Code_Example).ipynb`
- `Chapter_06_Planning_(Deep_Research_API).ipynb`

### Chapter 7: Multi-Agent Collaboration
- `Chapter_07_Multi_Agent_(ADK_Gemini_AgentTool).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Loop).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Parallel).ipynb`
- `Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb`
- `Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb`

### Chapter 8: Memory Management
- `Chapter_08_Memory_(ADK_Explicit_State_Update).ipynb`
- `Chapter_08_Memory_(ADK_LlmAgent_output_key).ipynb`
- `Chapter_08_Memory_(ADK_MemoryService_InMemory).ipynb`
- `Chapter_08_Memory_(ADK_SessionService).ipynb`
- `Chapter_08_Memory_(LangChain_LangGraph).ipynb`

### Chapter 9: Learning and Adaptation
- `Chapter_09_Adaptation_(OpenEvolve).ipynb`

### Chapter 10: Model Context Protocol (MCP)
- `Chapter_10_MCP_(ADK_FastMCP_Server).ipynb`
- `Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb`
- `Chapter_10_MCP_(FastMCP_Server_Example).ipynb`
- `Chapter_10_MCP_(Filesystem_Example_agent).ipynb`
- `Chapter_10_MCP_(Filesystem_Example_init).ipynb`

### Chapter 11: Goal Setting and Monitoring
- `Chapter_11_Goal_Setting_(Iteration).ipynb`

### Chapter 12: Exception Handling and Recovery
- `Chapter_12_Exception_Handling_(Fallback).ipynb`

### Chapter 13: Human-in-the-Loop
- `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb`

### Chapter 14: Knowledge Retrieval (RAG)
- `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb`
- `Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb`
- `Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb`

### Chapter 15: Inter-Agent Communication
- `Chapter_15_Inter_Agent_(A2A).ipynb`
- `Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb`
- `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb`

### Chapter 16: Resource-Aware Optimization
- `Chapter_16_Resource_Optimization_(Code_Snippets).ipynb`
- `Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb`

### Chapter 17: Reasoning Techniques
- `Chapter_17_Reasoning_(CoT_Prompt).ipynb`
- `Chapter_17_Reasoning_(Executing_Code).ipynb`
- `Chapter_17_Reasoning_(Google_DeepSearch).ipynb`
- `Chapter_17_Reasoning_(Self_Correction).ipynb`

### Chapter 18: Guardrails / Safety Patterns
- `Chapter_18_Guardrails_(ADK_Validate_Tool).ipynb`
- `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb`
- `Chapter_18_Guardrails_(Practical_Examples).ipynb`

### Chapter 19: Evaluation and Monitoring
- `Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb`
- `Chapter_19_Evaluation_(LLM_as_Judge).ipynb`

### Chapter 20: Prioritization
- `Chapter_20_Prioritization_(SuperSimplePM).ipynb`

### Chapter 21: Exploration and Discovery
- `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb`

### Appendices
- `Appendix_A_Advanced_Prompting_Techniques.ipynb`
- `Appendix_B_AI_Agentic_From_GUI_to_Real_world_environment.ipynb`
- `Appendix_C_(Code).ipynb`
- `Appendix_C_Quick_overview_of_Agentic_Frameworks.ipynb`
- `Appendix_D_Building_an_Agent_with_AgentSpace.ipynb`
- `Appendix_E_AI_Agents_on_the_CLI.ipynb`
- `Appendix_F_Under_the_Hood_Reasoning_Engines.ipynb`
- `Appendix_G_Coding_agents.ipynb`
- `Appendix_Pydantic.ipynb`

## Getting Started
Jupyter is optional and is not installed by this repository.

```bash
python3 -m pip install jupyter
cd chapter_notebooks
jupyter notebook
```

Open a specific notebook only after installing the imports that file uses. Supply API keys through your own environment. The notebooks that read keys expect names such as `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `DATASTORE_ID`, and `GOOGLE_CSE_ID`. This tree does not contain those values.

There is no `requirements.txt`. `pandas`, `numpy`, and `matplotlib` are not the dependency set of these notebooks. Imports that do appear include `langchain_openai`, `google.adk`, `crewai`, `openai`, `fastmcp`, `openevolve`, `langgraph`, and `google.generativeai`. Versions are unpinned and were not installed during the audit.

## Sources
These links are external pointers carried in from the notebook collection. They are not setup steps for the files already in this directory.

- [Table of Contents (Google Doc)](https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/edit) — external; the chapter list below is the in-repo index.
- [Google Drive folder](https://drive.google.com/drive/u/0/folders/1Y3U3IrYCiJ3E45Z8okR5eCg7OPnWQtPV) — historical source named by the seven placeholder notebooks. Access was not re-checked in the 2026-09-23 audit.
