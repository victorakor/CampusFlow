# Design Decisions

## Priority uses plain Python rules, not AI
Priority comes from `calculate_priority()` in `campusflow/tickets.py`. The rules
are checked in order and the first match wins, so results are predictable and
easy to test.

## Tickets are plain dictionaries in a list
No classes, no database. Keeps the code easy to read and lets the JSON file
map directly onto the in-memory data.

## JSON file for storage
`tickets.json` is human-readable and needs no extra packages. The file is saved
after every change. A damaged file stops the program with a clear message and
is never overwritten, so data is not lost by accident.

## One allowed status move per state
`NEXT_STATUS` in `campusflow/workflow.py` maps each status to the single status
it may move to (open -> in_progress -> resolved -> open). Steps cannot be
skipped, and a resolved ticket is locked until it is reopened.

## Menu code lives in `main.py`
The modules in `campusflow/` never print or ask for input. Only `main.py`
talks to the user, which keeps the rules testable without simulating typing.

## Module split
| Module | Responsibility |
|--------|----------------|
| `tickets.py` | What a ticket is, validation, priority, create/find |
| `workflow.py` | What can happen to a ticket after it exists |
| `storage.py` | Reading and writing the JSON file |
| `reports.py` | Counting tickets |
