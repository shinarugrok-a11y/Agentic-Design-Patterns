# Guardrails / Safety — Pattern reference

Load this file only when implementing `guardrails-safety`. Do not load by default.

## Book (Gulli) — rule of thumb
Use whenever autonomous agents can cause harm, leak data, or violate policy; stack filters before/after tools.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Guardrail design pattern (input/output filters, tool validation, layered defense).

## Notebooks (extracted)

Guardrails / Safety Patterns

### Notebooks
- `Chapter_18_Guardrails_(ADK_Validate_Tool).ipynb`
- `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` *(prompt text)*
- `Chapter_18_Guardrails_(Practical_Examples).ipynb`

### Patterns
- **before_tool_callback:** validate args against session state before tool execution; return error dict to block
- **LLM-as-guardrail:** pre-screen inputs; output JSON `{decision, reasoning}` or `{compliance_status, ...}`
- **CrewAI guardrails:** `Task(guardrail=validate_fn, output_pydantic=PolicyEvaluation)` with Pydantic validation
- **Default to safe/compliant** when ambiguous (explicit in prompts)

### Prompt templates
LLM guardrail decision protocol:
```
1.  Analyze the "Input to AI Agent" against **all** the "Guidelines for Unsafe Inputs."
2.  If the input clearly violates **any** of the guidelines, your decision is "unsafe."
3.  If you are genuinely unsure whether an input is unsafe (i.e., it's ambiguous or borderline), err on the side of caution and decide "safe."
```

CrewAI SAFETY_GUARDRAIL_PROMPT opening:
```
You are an AI Content Policy Enforcer, tasked with rigorously screening inputs intended for a primary AI system. Your core duty is to ensure that only content adhering to strict safety and relevance policies is processed.
```

Output format:
```json
{
 "compliance_status": "compliant" | "non-compliant",
 "evaluation_summary": "...",
 "triggered_policies": ["..."]
}
```

### Minimal code
```python
# ADK before_tool_callback
def validate_tool_params(tool, args, tool_context) -> Optional[Dict]:
    if args.get("user_id_param") != tool_context.state.get("session_user_id"):
        return {"status": "error", "error_message": "Tool call blocked: User ID validation failed."}
    return None  # allow execution

root_agent = Agent(..., before_tool_callback=validate_tool_params)
```

```python
# CrewAI guardrail task
evaluate_input_task = Task(
    description=f"{SAFETY_GUARDRAIL_PROMPT}\n\nUser Input: '{{user_input}}'",
    agent=policy_enforcer_agent,
    guardrail=validate_policy_evaluation,
    output_pydantic=PolicyEvaluation,
)
```

### Caveats
- Replace placeholder brand/competitor lists in prompts
- Practical Examples requires `GOOGLE_API_KEY` for Gemini Flash guardrail
- Guardrail defaulting to "compliant"/"safe" on ambiguity may allow borderline unsafe inputs
- `before_tool_callback` signature uses `ToolContext`, not `CallbackContext`

---

## Failure modes (skill-level)
- Ambiguity defaulted to 'safe'
- Placeholder brand lists never updated
- Callback on wrong context type

## Chains with
`human-in-the-loop`, `exception-handling`
