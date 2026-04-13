# SKILL — VOLUMIO 4 PLUGIN DEVELOPMENT V1

## Purpose
This skill gives coding agents a stable starting point for Volumio 4 plugin work in this repository.

## Read before coding
- `AGENTS.md`
- `components/AGENTS.md`
- `contracts/repo/naming_and_release_numbering_standard_v1.md`
- `contracts/repo/component_artifact_model_v1.md`

## Working assumptions
- target platform is Volumio 4 on Bookworm
- repository code should reflect actual Volumio plugin/runtime behavior, not guesswork
- plugin role should be explicit: source tile, user-interface plugin, helper service, overlay launcher, runtime renderer, hardware support, or similar

## Required questions the agent must answer in docs/journals
- what Volumio plugin category or runtime role does this artifact belong to?
- is it user-visible?
- does it open a screen, render a screen, provide a source tile, or run in the background?
- what install path is used?
- what rollback path is required?
- must Volumio unregistration happen on rollback?

## Preferred development pattern
1. identify the component
2. identify the artifact role(s)
3. map the payload path
4. map deploy candidate scripts
5. map rollback/unregistration expectations
6. update current-state docs if operational reality changes

## Volumio-specific expectations
- keep category and lifecycle explicit
- do not assume store-ready quality from imported payloads
- prefer repo-driven deploy/rollback semantics over Pi-local bootstrap assumptions
- keep plugin activation behavior and runtime side effects documented

## Repository references
Use the official Volumio developer docs and the reference repos listed in `docs/agents/reference_repositories_and_docs_v1.md`.
