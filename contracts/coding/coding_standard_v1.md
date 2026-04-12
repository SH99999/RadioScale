# CODING STANDARD V1

Status: authoritative integration standard.

## Purpose

This standard defines the minimum coding, commenting, logging and configuration quality requirements for all project code delivered into this repository.

## Leading rule

Every function must be documented with a clear comment or docstring.

The documentation must explain at least:
- purpose
- inputs
- outputs
- side effects
- failure behavior
- important dependencies

## Language-specific rules

### Bash and shell
- use `#!/usr/bin/env bash`
- use `set -euo pipefail`
- no silent fall-through on critical operations
- every script must print meaningful error output on failure
- no hardcoded GPIOs, paths, ports, service names or timing values without a documented constant or manifest reference

### JavaScript / Node / Volumio plugin code
- every exported function and every non-trivial internal function must carry a short doc comment
- plugin-facing contracts must be described near the function boundary
- no undocumented magic values
- config paths and plugin ids must be centralized and named
- asynchronous error paths must log meaningful context

### Python
- every function must have a docstring or a directly preceding clear comment
- no silent exception swallowing except with explicit reason and logging
- configuration values must be centralized and named

## Comment and docstring rule

A valid function comment or docstring must answer:
- what this function does
- what it expects
- what it changes
- what can fail

Short trivial getters may use concise comments, but component integration functions, install hooks, health checks, uninstall hooks and hardware logic must always be fully documented.

## Logging rule

Code must use stable, searchable log prefixes where practical.
The preferred prefixes are:
- `SR_STARTER`
- `SR_TUNER`
- `SR_AUTOSWITCH`
- `SR_BRIDGE`
- `SR_FUNLINE`
- `SR_HW`
- `SR_DEPLOY`

## Configuration rule

Configuration must be contract-driven, not scattered.
The preferred order is:
1. manifest-defined values
2. named constants
3. environment variables if explicitly documented

## Forbidden patterns

- undocumented GPIO or path literals
- undocumented service name usage
- hidden contract changes in component branches
- missing function comments on integration-relevant functions
- silent fallback behavior without comment
- unlogged catch-all failures in runtime-critical paths

## Quality gate

A contribution fails this standard if:
- integration-relevant functions are undocumented
- install/configure/healthcheck/uninstall hooks are undocumented
- runtime-critical code uses unexplained magic values
- contract-relevant changes are made without comment or manifest alignment
