"""Memory management: scoped session state + searchable long-term store.

Offline stub mirroring ADK ideas: prefixed state keys (user:/app:/temp:),
updates through a tool context (never mutate raw state directly), and a
tiny long-term store with search.
"""
import time
from dataclasses import dataclass, field


@dataclass
class Session:
    state: dict = field(default_factory=dict)
    events: list = field(default_factory=list)


class ToolContext:
    """Tools update state through this object so changes are recorded as events."""
    def __init__(self, session: Session):
        self._session = session
        self.state = session.state

    def commit(self, author: str):
        self._session.events.append({"author": author, "state_delta": dict(self.state)})


def log_user_login(tool_context: ToolContext) -> dict:
    s = tool_context.state
    s["user:login_count"] = s.get("user:login_count", 0) + 1      # persists across sessions
    s["task_status"] = "active"                                   # session scope
    s["user:last_login_ts"] = time.time()
    s["temp:validation_needed"] = True                            # discarded after invocation
    tool_context.commit("log_user_login")
    return {"status": "success", "message": f"logins={s['user:login_count']}"}


class LongTermStore:
    def __init__(self):
        self._items: dict[tuple, dict] = {}

    def put(self, namespace: tuple, key: str, value: dict):
        self._items[namespace + (key,)] = value

    def search(self, namespace: tuple, query: str) -> list[dict]:
        q = set(query.lower().split())
        hits = [(len(q & set(str(v).lower().split())), v)
                for k, v in self._items.items() if k[:len(namespace)] == namespace]
        return [v for score, v in sorted(hits, key=lambda h: -h[0]) if score]


def end_of_invocation(session: Session):
    for k in [k for k in session.state if k.startswith("temp:")]:
        del session.state[k]


if __name__ == "__main__":
    session = Session(state={"user:login_count": 0, "task_status": "idle"})
    print(log_user_login(ToolContext(session)))
    end_of_invocation(session)
    print("state:", session.state)

    store = LongTermStore()
    store.put(("user-1", "prefs"), "a-memory", {"rules": ["short direct language", "english and python"]})
    print("search:", store.search(("user-1",), "language preferences python"))
