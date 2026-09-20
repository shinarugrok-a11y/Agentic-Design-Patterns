"""Prompt chaining: two-stage extract -> transform pipeline.

Runs without any API key using a stub LLM. Swap `llm` for a real model
(e.g. `ChatOpenAI(temperature=0)` piped through LCEL) in production.
"""
import json
import re


def llm(prompt: str) -> str:
    """Stub model: deterministic behaviour for the two stage prompts."""
    if prompt.startswith("Extract"):
        text = prompt.split("\n\n", 1)[1]
        cpu = re.search(r"([\d.]+ GHz [\w-]+)", text)
        mem = re.search(r"(\d+GB)", text)
        sto = re.search(r"(\d+TB \w+ SSD)", text)
        return f"cpu={cpu.group(1)}; memory={mem.group(1)}; storage={sto.group(1)}"
    if prompt.startswith("Transform"):
        specs = prompt.split("\n\n", 1)[1]
        pairs = dict(p.split("=", 1) for p in specs.split("; "))
        return json.dumps(pairs)
    raise ValueError("unknown stage")


def stage_extract(text_input: str) -> str:
    return llm(f"Extract the technical specifications from the following text:\n\n{text_input}")


def stage_transform(specifications: str) -> str:
    return llm("Transform the following specifications into a JSON object with "
               f"'cpu', 'memory', and 'storage' as keys:\n\n{specifications}")


def chain(text_input: str) -> dict:
    specs = stage_extract(text_input)          # stage 1 output ...
    return json.loads(stage_transform(specs))  # ... is stage 2 input


if __name__ == "__main__":
    raw = "The new laptop features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."
    print(chain(raw))
