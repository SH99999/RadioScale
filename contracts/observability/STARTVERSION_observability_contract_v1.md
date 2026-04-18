# STARTVERSION Observability Contract v1

## Goal
Every important change must be diagnosable.

## Minimum signals
- version/release identifier
- execution outcome (success/failure)
- error reason on failure
- timestamp

## Operational rule
- If a failure cannot be diagnosed from logs/status, the package is not complete.
