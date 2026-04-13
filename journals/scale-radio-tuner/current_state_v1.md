# CURRENT STATE — scale-radio-tuner

## Component
- normalized component name: `scale-radio-tuner`
- governed artifact pattern: one component with multiple artifacts
- active artifacts in the current baseline:
  - `Scale FM Overlay`
  - `Scale FM Source`
  - resident renderer service `scale_fm_renderer.service`
- active work lane: `dev/tuner`

## Repo truth
- component root exists at `components/scale-radio-tuner/`
- dedicated branch `dev/tuner` exists and is the active tuner work lane
- tuner is governed as one component with multiple artifacts, not as separate branches per plugin

## Lifecycle status
- `payload_complete`
- `functional_acceptance_open`

## Accepted baseline
- authoritative baseline: resident-renderer lineage culminating in `1.10.2`
- external names:
  - `Scale FM Overlay`
  - `Scale FM Source`
- internal identifiers that must remain stable:
  - `radio_scale_peppy`
  - `radio_scale_source`
  - `scale_fm_renderer.service`

## Current known working behavior
- tuner opens via source tile and via the locked public call-method contract
- resident renderer baseline exists and the classic spawn fallback remains required
- snap/lock, hiss, and reopen behavior are materially improved versus earlier builds
- long-press exit cooperates with Now Playing well enough for the current baseline
- shared overlay-owner handling through `/tmp/mediastreamer_active_overlay.json` is part of the governed design

## Current gaps
- latest `1.10.2` baseline still needs targeted runtime validation on the target Pi
- first-show pointer sweep after boot remains unresolved
- exit white flashes remain unresolved
- pointer flicker/jitter is not fully solved
- OE1 cleanup in persisted lists remains incomplete
- tuner does not yet have the same repo-driven deploy maturity as bridge

## Repo-normalized next action
1. validate `1.10.2` on target Pi without changing public method or service-name contracts
2. confirm deep-idle behavior and shared-owner arbitration in real runtime
3. isolate first-show pointer hydration order
4. reduce exit white flashes without breaking the current call-method/service contract
