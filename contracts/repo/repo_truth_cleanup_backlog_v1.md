# REPO TRUTH CLEANUP BACKLOG V1

## Purpose
This backlog records where current repository truth is still incomplete or uncertain and needs explicit normalization.

## Highest priority
### 1. scale-radio-starter
Current uncertainty:
- exact component-path/payload/source tree still not cleanly grounded from surviving context
- exact stable asset inventory for `v0.2.2 stable` remains uncertain
Required action:
- verify actual files in repo
- map accepted stable baseline into explicit repo paths
- update README/journal with final repo truth

### 2. scale-radio-fun-line
Current uncertainty:
- exact repo-normalized payload structure for overlay/source/future packs remains unresolved
- latest nonleading builds need clearer repo labeling as partial/experimental
Required action:
- lock repo truth around `0.4.2`
- identify where later 0.5.0/0.6.0 material lives and mark it explicitly nonleading
- normalize overlay/source/packs structure under component governance

### 3. scale-radio-hardware
Current uncertainty:
- source-of-truth under `components/scale-radio-hardware/` still incomplete
- standalone AS5600 tester source and related docs/mechanical assets need normalization
Required action:
- commit/normalize source, wiring docs, and validation-lane structure
- keep component on `dev/hardware` until live validation exists

## Medium priority
### 4. scale-radio-tuner
Current uncertainty:
- exact payload subtree naming in repo versus governed artifact model could be clearer
- deploy lane maturity still trails bridge
Required action:
- align payload naming with artifact model and release numbering rules
- define the next deploy candidate lane after validation

### 5. scale-radio-bridge
Current uncertainty:
- whether `0.2.3_db_cache_r1` becomes the next locked stable baseline
Required action:
- keep `rsob_022sf22l.zip` as rollback anchor until field validation completes
- promote or reject the DB-cache branch explicitly

### 6. scale-radio-autoswitch
Current uncertainty:
- future technology shape may change from bash/systemd to plugin-based
Required action:
- if that migration begins, use the technology-change process before changing repo truth

## Rule
No uncertain area should stay hidden. It must be either:
- normalized into repo truth, or
- explicitly listed here as unresolved.
