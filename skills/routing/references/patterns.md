# Routing

Ch 2.

## Frameworks
- Google ADK (Agent, InMemoryRunner, FunctionTool); LangGraph (RunnableBranch); plain OpenRouter HTTP.

## Key APIs from the notebooks
- `ADK: booking_handler / info_handler / unclear_handler registered as specialist functions`
- `ADK: run_coordinator(runner, request) classifies then dispatches; main() wires runner`
- `LangGraph: RunnableBranch routes on classifier output; RunnablePassthrough keeps input`

## Code patterns
- Pattern: coordinator (classifier) -> specialist handler -> response; always include an unclear/fallback handler.
- Keep handlers pure functions of the request string for testability.
- Log the chosen route with each request for evaluation.

## Prompt templates
- Classifier: `Classify this request as booking|info|unclear. Reply with one word: {request}`
- Specialist: `You handle {route} requests only. If out of scope, say UNCLEAR: {request}`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_02_Routing_(Google_ADK).ipynb`
- `chapter_notebooks/Chapter_02_Routing_(LangGraph).ipynb`
- `chapter_notebooks/Chapter_02_Routing_(Openrouter).ipynb`

