# STARTVERSION Volumio4 Contract v1

## Scope
Volumio4 plugin and integration behavior.

## Rules
- Keep plugin config deterministic and explicit.
- Avoid hidden defaults for critical runtime behavior.
- Changes to plugin behavior require validation steps and rollback note.

## Acceptance minimum
- config impact described
- runtime check command(s) included
- rollback path included
