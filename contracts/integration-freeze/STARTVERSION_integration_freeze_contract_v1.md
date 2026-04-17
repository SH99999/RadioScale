# STARTVERSION Integration Freeze Contract v1

## Purpose
Prevent unstable cross-component merges.

## Freeze triggers
- repeated integration regressions
- unresolved critical dependency conflicts
- failing deploy/rollback on target environment

## During freeze
- allow only fixes that reduce risk or restore determinism
- block new scope until freeze exit criteria pass

## Exit criteria
- failing checks resolved
- dependency conflicts resolved
- owner accepts freeze exit in PR decision
