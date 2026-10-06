"""A2A: discover a remote agent by its Agent Card, then send it a task.

Offline stub of the protocol shape (card discovery -> skill match ->
JSON-RPC sendTask -> task state handling). No network involved.
"""
import json
import uuid

AGENT_CARD = {
    "name": "WeatherBot", "url": "http://weather-service.example.com/a2a", "version": "1.0.0",
    "capabilities": {"streaming": True}, "authentication": {"schemes": ["apiKey"]},
    "skills": [
        {"id": "get_current_weather", "description": "Retrieve real-time weather for any location.",
         "examples": ["What's the weather in Paris?"], "tags": ["weather", "current"]},
        {"id": "get_forecast", "description": "Get 5-day weather predictions.",
         "examples": ["5-day forecast for New York"], "tags": ["weather", "forecast"]},
    ],
}


def remote_server(request: dict) -> dict:
    """Stand-in for the remote agent's HTTP endpoint."""
    text = request["params"]["message"]["parts"][0]["text"]
    if "forecast" in text.lower() and "for" not in text.lower().split():
        return {"jsonrpc": "2.0", "id": request["id"],
                "result": {"id": request["params"]["id"], "status": {"state": "input-required"},
                           "message": "Which city?"}}
    return {"jsonrpc": "2.0", "id": request["id"],
            "result": {"id": request["params"]["id"], "status": {"state": "completed"},
                       "artifacts": [{"parts": [{"type": "text", "text": f"Result for: {text}"}]}]}}


def pick_skill(card: dict, intent: str) -> str | None:
    words = set(intent.lower().split())
    def overlap(s):
        return len(words & set(s["tags"]) | (words & set(s["description"].lower().split())))
    best = max(card.get("skills", []), key=overlap, default=None)
    return best["id"] if best and overlap(best) else None      # no match: do not delegate


def send_task(card: dict, text: str, session_id: str, task_id: str | None = None) -> dict:
    if not isinstance(text, str) or not text.strip() or len(text) > 2000:
        raise ValueError("task text must be a non-empty string of at most 2000 characters")
    if not card.get("url", "").startswith(("https://", "http://")):
        raise ValueError("agent card has no usable url")
    method = "sendTaskSubscribe" if card["capabilities"].get("streaming") else "sendTask"
    request = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": method,
               "params": {"id": task_id or f"task-{uuid.uuid4().hex[:6]}", "sessionId": session_id,
                          "message": {"role": "user", "parts": [{"type": "text", "text": text}]},
                          "acceptedOutputModes": ["text/plain"], "historyLength": 5}}
    return remote_server(request)["result"]


if __name__ == "__main__":
    session = "session-001"
    print("skill:", pick_skill(AGENT_CARD, "5-day forecast for London"))
    assert pick_skill(AGENT_CARD, "book me a flight") is None
    task = send_task(AGENT_CARD, "Give me the forecast", session)
    print(json.dumps(task))
    first_id = task["id"]
    if task["status"]["state"] == "input-required":          # multi-turn: reply in the same task
        task = send_task(AGENT_CARD, "5-day forecast for London", session, task_id=first_id)
    print(json.dumps(task))
    assert task["id"] == first_id and task["status"]["state"] == "completed"
