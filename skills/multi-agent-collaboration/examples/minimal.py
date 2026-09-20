"""Multi-agent collaboration: a coordinator hands one goal down a chain of specialists, each reading and writing shared state.

Real framework: Google ADK LlmAgent(sub_agents=[researcher, analyst, writer]) with output_key writing to session.state
Run: python3 examples/minimal.py
"""

CANNED = {
    "researcher": "3 sources on agent memory",
    "analyst": "ranking: vector store > buffer",
    "writer": "Brief: use a vector store for recall.",
}


def llm(name: str, prompt: str) -> str:
    """Fake specialist model: canned output per role."""
    return CANNED[name]


class Agent:
    def __init__(self, name, instruction, output_key, reads=None):
        self.name = name
        self.instruction = instruction
        self.output_key = output_key
        self.reads = reads

    def run(self, state):
        upstream = state[self.reads] if self.reads else "(none)"
        result = llm(self.name, f"{self.instruction}\nContext: {upstream}")
        state[self.output_key] = result
        print(f"[{self.name}] got {upstream!r} -> state['{self.output_key}'] = {result!r}")


researcher = Agent("researcher", "Find sources on the topic.", "findings")
analyst = Agent("analyst", "Rank what is in state['findings'].", "analysis", reads="findings")
writer = Agent("writer", "Write a brief from state['analysis'].", "brief", reads="analysis")


def coordinator(goal, sub_agents):
    """Sequential handoff: the coordinator owns the order, shared state carries the context."""
    print(f"coordinator: delegating {goal!r} to {[a.name for a in sub_agents]}")
    state = {}
    for agent in sub_agents:
        agent.run(state)
    return state["brief"]


print("final:", coordinator("summarize agent memory options", [researcher, analyst, writer]))
