"""Chapter 14 — Minimal retrieve → generate graph (LangGraph RAG)."""
from langgraph.graph import StateGraph, END

def build_rag(retrieve_node, generate_node, state_cls):
    g = StateGraph(state_cls)
    g.add_node("retrieve", retrieve_node)
    g.add_node("generate", generate_node)
    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "generate")
    g.add_edge("generate", END)
    return g.compile()
