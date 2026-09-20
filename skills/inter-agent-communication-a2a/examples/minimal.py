"""Discover a peer via its Agent Card, send a task, poll it to a terminal state.

Real framework: A2A over JSON-RPC — GET /.well-known/agent.json, then
tasks/send followed by polling until state is completed or input-required.
Run: python3 examples/minimal.py
"""

AGENT_CARD = {
    "name": "WeatherBot", "url": "http://peer.example/a2a",
    "capabilities": {"streaming": False},
    "skills": [{"id": "get_forecast", "examples": ["5-day forecast for New York"]}],
}
_STATES = ["submitted", "working", "input-required", "working", "completed"]


def peer_call(method: str, params: dict) -> dict:
    """Fake A2A server: walks one task through the protocol's state machine."""
    task = params["task"]
    task["state"] = _STATES[min(task["polls"], len(_STATES) - 1)]
    task["polls"] += 1
    if task["state"] == "input-required":
        task["prompt"] = "Which city?"
    if task["state"] == "completed":
        task["artifact"] = "New York: sunny, 21C"
    return {"jsonrpc": "2.0", "result": task}


def delegate(request: str) -> str:
    if not AGENT_CARD["skills"]:
        return "no capable peer; not delegating"
    task = {"id": "task-001", "contextId": "ctx-1", "polls": 0, "state": "submitted"}
    print(f"discovered {AGENT_CARD['name']} skill={AGENT_CARD['skills'][0]['id']}")
    for _ in range(8):
        task = peer_call("tasks/send", {"task": task, "message": request})["result"]
        print(f"  task {task['id']} state={task['state']}")
        if task["state"] == "input-required":
            request = "New York"          # same task id and contextId
        elif task["state"] in ("completed", "failed", "canceled"):
            return task.get("artifact", task["state"])
    return "deadline exceeded; task orphaned"


print(f"result: {delegate('what is the forecast?')}")
