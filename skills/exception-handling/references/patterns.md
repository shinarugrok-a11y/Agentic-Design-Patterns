# Exception Handling and Recovery

Ch 12.

## Frameworks
- Google ADK (SequentialAgent primary -> fallback composition).

## Key APIs from the notebooks
- `SequentialAgent([primary_agent, fallback_agent]) chain`
- `43-line notebook: fallback agent takes over when primary raises/fails`
- `Degraded-response flagging on fallback path`

## Code patterns
- Pattern: classify error (transient/fatal) -> retry w/ backoff -> fallback agent -> degraded flag.
- Never retry fatal/validation errors.
- Always flag fallback-sourced answers as degraded.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_12_Exception_Handling_(Fallback).ipynb`

