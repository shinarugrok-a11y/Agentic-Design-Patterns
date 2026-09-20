"""Two-stage chain: extract specs from prose, then transform them into JSON.

Real framework: LangChain LCEL
  extract = prompt_extract | llm | StrOutputParser()
  chain = {"specifications": extract} | prompt_transform | llm | StrOutputParser()
Run: python3 examples/minimal.py
"""

import json

PROMPT_EXTRACT = "Extract the technical specifications from:\n\n{text_input}"
PROMPT_TRANSFORM = (
    "Transform these specifications into a JSON object with 'cpu', 'memory',"
    " and 'storage' as keys:\n\n{specifications}"
)


def llm(prompt: str) -> str:
    """Canned stand-in for a model call; keyed on which stage prompt it sees."""
    if prompt.startswith("Extract"):
        return "CPU: 3.5 GHz octa-core; Memory: 16GB RAM; Storage: 1TB NVMe SSD"
    return json.dumps({"cpu": "3.5 GHz octa-core", "memory": "16GB", "storage": "1TB NVMe SSD"})


def extract(text_input: str) -> str:
    return llm(PROMPT_EXTRACT.format(text_input=text_input))


def transform(specifications: str) -> str:
    return llm(PROMPT_TRANSFORM.format(specifications=specifications))


raw_text = "The new laptop features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."

# Stage 1 output becomes stage 2 input; validate at the seam so a bad
# extraction fails here instead of being confidently reformatted downstream.
specs = extract(raw_text)
print("stage 1 (extract):", specs)
assert ":" in specs, "stage 1 produced no parseable specifications"

result = transform(specs)
print("stage 2 (transform):", result)
print("parsed:", json.loads(result))
