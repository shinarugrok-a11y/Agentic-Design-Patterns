"""Exception handling: retry transient errors, fall back, degrade honestly.

Offline stub of the Chapter 12 primary -> fallback -> response pipeline with
failure recorded in shared state.
"""
import random

random.seed(3)


class TransientError(Exception):
    pass


def get_precise_location(address: str, state: dict) -> dict:
    if random.random() < 0.7:                       # flaky external service
        raise TransientError("geocoder timeout")
    state["location_result"] = f"precise coordinates for {address!r}"
    return {"status": "success"}


def get_general_area(city: str, state: dict) -> dict:
    state["location_result"] = f"approximate area for {city!r}"
    return {"status": "success", "degraded": True}


def with_retry(fn, *args, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            return fn(*args)
        except TransientError as e:
            print(f"  attempt {attempt + 1} failed: {e}")
    raise TransientError("retries exhausted")


def primary_handler(address: str, state: dict):
    try:
        with_retry(get_precise_location, address, state)
    except TransientError:
        state["primary_failed"] = True             # failure becomes state, not a crash


def fallback_handler(query: str, state: dict):
    if state.get("primary_failed"):
        city = query.split(",")[-1].strip()
        get_general_area(city, state)


def response_agent(state: dict) -> str:
    if not state.get("location_result"):
        return "Sorry, I could not retrieve the location."  # explicit empty branch
    note = " (approximate)" if state.get("primary_failed") else ""
    return f"Location: {state['location_result']}{note}"


if __name__ == "__main__":
    query = "1600 Amphitheatre Pkwy, Mountain View"
    state: dict = {}
    primary_handler(query, state)
    fallback_handler(query, state)
    print(response_agent(state))
