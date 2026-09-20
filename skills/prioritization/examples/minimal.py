"""Prioritization — minimal runnable demo (stdlib only)."""
tasks = [{'name': 'fix login', 'p': 0}, {'name': 'tweak logo', 'p': 2}, {'name': 'add SSO', 'p': 1}]
queue = sorted(tasks, key=lambda t: t['p'])
workers = ['w1', 'w2']
for task, w in zip(queue, workers * 2):
    print(w + ' <- ' + task['name'] + ' (P' + str(task['p']) + ')')
