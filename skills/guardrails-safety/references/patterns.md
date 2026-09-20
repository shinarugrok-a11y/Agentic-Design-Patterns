# Guardrails and Safety

Ch 18.

## Frameworks
- Google ADK (validate_tool_params, BaseTool/ToolContext); CrewAI + pydantic guardrail crew.

## Key APIs from the notebooks
- `ADK: validate_tool_params(tool, params, ToolContext) pre-call gate`
- `LLM_as_Guardrail notebook: LLM judge verdict pattern`
- `Practical notebook: PolicyEvaluation(BaseModel); validate_policy_evaluation(output); run_guardrail_crew(user_input) -> (compliant, message, flags)`

## Code patterns
- Pattern: gate input -> gate tool params -> gate output; log every verdict.
- Pydantic schemas for deterministic gates; LLM judges only for nuance.
- Return (allow, message, flags) triples for audit.

## Prompt templates
- Judge: `Policy: {rules}. Classify input as COMPLIANT or VIOLATION + reason: {input}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_18_Guardrails_(ADK_Validate_Tool).ipynb`
- `chapter_notebooks/Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb`
- `chapter_notebooks/Chapter_18_Guardrails_(Practical_Examples).ipynb`

