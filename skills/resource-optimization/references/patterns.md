# Resource-Aware Optimization

Ch 16.

## Frameworks
- Google ADK (QueryRouterAgent BaseAgent); OpenAI API + HTTP search.

## Key APIs from the notebooks
- `ADK: QueryRouterAgent(BaseAgent)._run_async_impl routes by query type`
- `OI notebook: classify_prompt(prompt) -> dict; google_search(query) -> list; generate_response(prompt, classification, search_results); handle_prompt(prompt) -> dict`
- `handle_prompt returns response + cost/route accounting`

## Code patterns
- Pattern: classify difficulty -> cheapest sufficient tier -> respond -> log cost/quality.
- Tiers: direct answer (cheap) / search-augmented / frontier reasoning.
- Always log route + cost + quality for review.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_16_Resource_Optimization_(Code_Snippets).ipynb`
- `chapter_notebooks/Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb`

