"""Memory Management — minimal runnable demo (stdlib only)."""
store = {}

def remember(user, key, value):
    store.setdefault(user, {})[key] = value

def recall(user, key, default=None):
    return store.get(user, {}).get(key, default)

remember("ana", "city", "Lisbon")
print("Ana city:", recall("ana", "city"))
print("Bob city:", recall("bob", "city", "unknown"))
