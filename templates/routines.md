# Routines (template): bounded cron and self-expiring watches

DERIVED/operational, not from the book. Every routine has a hard end, so a forgotten one stops by itself. Unknown or missing bounds mean the routine is BLOCKED and does not start.

## Bounded cron
```yaml
name: <routine name>
schedule: <cron expression>
max_runs: <N>                 # required; stop after N runs
expires_at: <ISO 8601 time>   # required; stop at this time even if runs remain
on_each_run: <read-only check or draft; consequential actions follow gate G2>
on_failure: stop and report   # never retry forever
```

## Self-expiring watch
```yaml
watch: <what to observe, read-only>
until: <condition that ends the watch>
expires_at: <ISO 8601 time>   # required; the watch ends here even if `until` never holds
report_to: <role, not an address>
```

Rules: a routine never grants itself new connectors or scopes (gate G5) and never sends without APPROVE (gate G2). Renewal is a new human decision, not an automatic extension.
