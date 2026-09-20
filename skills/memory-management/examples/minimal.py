"""Memory: short-term state changes go through an event delta, and facts persisted to long-term memory are recalled in a later session.

Real framework: ADK session_service.append_event(session, Event(actions=EventActions(state_delta=...))) plus memory_service.add_session_to_memory / search_memory
Run: python3 examples/minimal.py
"""

LONG_TERM = []


class Session:
    def __init__(self, session_id, user_id):
        self.id, self.user_id = session_id, user_id
        self.state, self.events = {}, []


def append_event(session, state_delta, text=""):
    """The only way state changes: as a delta carried by an appended event."""
    session.events.append({"state_delta": state_delta, "text": text})
    session.state.update(state_delta)


def add_session_to_memory(session):
    """Persist durable state only; temp: keys never leave the session."""
    facts = {k: v for k, v in session.state.items() if not k.startswith("temp:")}
    LONG_TERM.append({"user_id": session.user_id, "facts": facts})


def search_memory(query, user_id):
    return [value for record in LONG_TERM if record["user_id"] == user_id
            for key, value in record["facts"].items() if query in key]


def llm(prompt: str) -> str:
    """Fake model: answers only from what the prompt contains."""
    return f"Rebooking you on {prompt.split(': ')[-1]}."


first = Session("s1", "u1")
append_event(first, {"user:preferred_airline": "Lufthansa", "temp:draft": "scratch"},
             text="user states a preference")
print(f"turn 1 state: {first.state}")
print(f"turn 1 events recorded: {len(first.events)}")

add_session_to_memory(first)
print(f"long-term store: {LONG_TERM}")

later = Session("s2", "u1")
print(f"new session starts empty: {later.state}")

hits = search_memory("airline", user_id="u1")
append_event(later, {"recalled_airline": hits[0]}, text="memory recall")
print(f"recalled {hits} -> state: {later.state}")
print(llm(f"Book a flight. Known preference: {later.state['recalled_airline']}"))
