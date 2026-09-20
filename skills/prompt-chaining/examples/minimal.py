"""Prompt Chaining — minimal runnable demo (stdlib only)."""
def llm(prompt):
    return f"[{len(prompt)}ch] " + prompt[:60]

text = open(__import__("sys").argv[1]).read() if len(__import__("sys").argv) > 1 else "Acme X1: 8GB RAM, 256GB SSD."
specs = llm(f"Extract technical specifications from: {text}")
table = llm(f"Format as JSON table: {specs}")
print(llm(f"Summarize for executives: {table}"))
