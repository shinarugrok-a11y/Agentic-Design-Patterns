"""Exception handling: retry transient errors, fall back, degrade honestly.

Offline stub of the Chapter 12 primary -> fallback -> response pipeline
(book GT:L7666-L7714). The state keys match the book. The book never defines
the tools or says what sets state["primary_location_failed"]; the tool bodies
and the flag-setting below are ours (DERIVED), not from the book.
"""
import random

random.seed(3)


class TransientError(Exception):
    pass


def get_precise_location_info(address: str, state: dict) -> dict:
    if random.random() < 0.7:                       # flaky external service
        raise TransientError("geocoder timeout")
    state["location_result"] = f"precise coordinates for {address!r}"
    return {"status": "success"}


def get_general_area_info(city: str, state: dict) -> dict:
    state["location_result"] = f"approximate area for {city!r}"
    return {"status": "success", "degraded": True}


def with_retry(fn, *args, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            return fn(*args)
        except TransientError as e:
            print(f"  [log] attempt {attempt + 1} failed: {type(e).__name__}")
    raise TransientError("retries exhausted")


def primary_handler(address: str, state: dict):
    if not isinstance(address, str) or not address.strip():
        raise ValueError("address must be a non-empty string")   # deterministic: do not retry
    try:
        with_retry(get_precise_location_info, address, state)
        state["primary_location_failed"] = False
    except TransientError:
        state["primary_location_failed"] = True     # failure becomes state, not a crash


def fallback_handler(query: str, state: dict):
    if state.get("primary_location_failed"):
        city = query.split(",")[-1].strip()
        get_general_area_info(city, state)


def response_agent(state: dict) -> str:
    if not state.get("location_result"):
        return "Sorry, I could not retrieve the location."  # explicit empty branch
    note = " (approximate)" if state.get("primary_location_failed") else ""
    return f"Location: {state['location_result']}{note}"


if __name__ == "__main__":
    query = "1600 Amphitheatre Pkwy, Mountain View"
    state: dict = {}
    primary_handler(query, state)
    fallback_handler(query, state)
    print(response_agent(state))
