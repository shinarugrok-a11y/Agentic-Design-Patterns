"""Routing — minimal runnable demo (stdlib only)."""
def classify(req):
    r = req.lower()
    return "booking" if any(k in r for k in ("book", "flight", "hotel")) else "info" if "?" in r else "unclear"

def booking_handler(r): return f"Booking flow for: {r}"
def info_handler(r): return f"Info answer for: {r}"
def unclear_handler(r): return f"Could you clarify: {r}"

req = __import__("sys").argv[1] if len(__import__("sys").argv) > 1 else "Book a flight to Rome?"
print({"booking": booking_handler, "info": info_handler, "unclear": unclear_handler}[classify(req)](req))
