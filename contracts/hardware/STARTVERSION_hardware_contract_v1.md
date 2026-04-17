# STARTVERSION Hardware Contract v1

## Scope
Hardware interaction, configuration, and boundary safety.

## Rules
- Treat hardware constraints as hard boundaries.
- Any hardware-affecting change must document:
  - supported devices/paths
  - failure mode
  - recovery steps
- Never assume unavailable hardware in CI; use explicit guards.

## Merge minimum
- Hardware risk statement present.
- Rollback/recovery path present.
