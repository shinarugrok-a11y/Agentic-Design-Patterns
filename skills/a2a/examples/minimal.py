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
    if "forecast" in text.lower() and "for" not in text.lower():
        return {"jsonrpc": "2.0", "id": request["id"],
                "result": {"id": request["params"]["id"], "status": {"state": "input-required"},
                           "message": "Which city?"}}
    return {"jsonrpc": "2.0", "id": request["id"],
            "result": {"id": request["params"]["id"], "status": {"state": "completed"},
                       "artifacts": [{"parts": [{"type": "text", "text": f"Result for: {text}"}]}]}}


def pick_skill(card: dict, intent: str) -> str | None:
    words = set(intent.lower().split())
    best = max(card["skills"], key=lambda s: len(words & set(s["tags"]) | (words & set(s["description"].lower().split()))))
    return best["id"]


def send_task(card: dict, text: str, session_id: str) -> dict:
    method = "sendTaskSubscribe" if card["capabilities"].get("streaming") else "sendTask"
    request = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": method,
               "params": {"id": f"task-{uuid.uuid4().hex[:6]}", "sessionId": session_id,
                          "message": {"role": "user", "parts": [{"type": "text", "text": text}]},
                          "acceptedOutputModes": ["text/plain"], "historyLength": 5}}
    return remote_server(request)["result"]


if __name__ == "__main__":
    session = "session-001"
    print("skill:", pick_skill(AGENT_CARD, "5-day forecast for London"))
    task = send_task(AGENT_CARD, "Give me the forecast", session)
    print(json.dumps(task))
    if task["status"]["state"] == "input-required":          # multi-turn: answer and resend
        task = send_task(AGENT_CARD, "5-day forecast for London", session)
    print(json.dumps(task))
