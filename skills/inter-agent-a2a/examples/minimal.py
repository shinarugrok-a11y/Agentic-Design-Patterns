"""Inter-Agent Communication (A2A) — minimal runnable demo (stdlib only)."""
CARDS = {'weather': {'endpoint': 'svc://weather', 'caps': ['forecast']}}

def a2a_request(card, task):
    return '[' + card['endpoint'] + '] result for ' + task

card = CARDS['weather']
assert 'forecast' in card['caps'], 'capability missing'
print(a2a_request(card, 'forecast Lisbon'))
