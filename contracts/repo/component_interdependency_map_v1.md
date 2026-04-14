# COMPONENT INTERDEPENDENCY MAP V1

## Purpose
This document records the current liveable interdependency model between active components.

## Leading rule
Dependencies should be explicit, minimal, and stable enough that one component can evolve without forcing hidden changes into another.

## Layer view
### Base runtime layer
- `scale-radio-starter`
- provides startup/runtime glue and accepted startup baseline
- other components should not assume this layer solved unrelated renderer performance questions unless separately documented

### Experience/runtime components
- `scale-radio-tuner`
- `scale-radio-fun-line`
- `scale-radio-autoswitch`
- `scale-radio-bridge`

### Hardware/input layer
- `scale-radio-hardware`
- future production relation to frontpanel-engine remains open

## Liveable dependency rules
### scale-radio-starter
Depends on:
- Volumio / touch_display / kiosk runtime
Provides to others:
- base runtime startup and handover environment
Must not silently absorb feature ownership from tuner, fun-line, or bridge.

### scale-radio-tuner
Depends on:
- starter/runtime base
- overlay owner coordination file
- hardware/input path later, but not yet as a governed hard dependency
Provides to others:
- primary Radio Scale visible experience
- shared overlay-owner participation
Must not depend on bridge for core opening/renderer ownership.

### scale-radio-fun-line
Depends on:
- starter/runtime base
- coexistence rules with tuner
Provides to others:
- overlay / experience layer only
Liveable rule:
- tuner and fun-line may coexist on the same system, but must not run as two heavy active renderers simultaneously.

### scale-radio-bridge
Depends on:
- starter/runtime base
- Volumio/plugin runtime
Provides to others:
- provider-layer metadata enrichment, lyrics, Spotify match, playlist add, caching
Liveable rule:
- bridge is provider-layer only and must not take renderer/controller ownership.

### scale-radio-autoswitch
Depends on:
- HiFiBerry ADC hardware path
- ALSA/systemd runtime
Provides to others:
- tape-active / analog-input switching behavior
Liveable rule:
- renderer/UI should consume exported state from autoswitch, but autoswitch should not own renderer behavior.
- source-restore ownership must be explicitly decided before coupling deeper into source/runtime logic.

### scale-radio-hardware
Depends on:
- physical donor-hardware assembly and validation
Provides to others:
- validated physical input path for later runtime integration
Liveable rule:
- hardware validation may proceed standalone before being treated as a hard tuner dependency.
- tuner real-world flywheel behavior becomes more meaningful after hardware validation, but tuner governance must not stall entirely on hardware.

## Current critical live dependencies
- tuner <-> fun-line: shared overlay ownership and deep-idle coexistence
- starter -> all runtime components: startup/handover base
- bridge -> tuner/fun-line/other consumers: provider-layer metadata only
- autoswitch -> future renderer/source consumers: exported tape-active state still needed
- hardware -> future tuner/input realism: real dependency later, partial dependency now

## Open dependency decisions
- exact tuner <- hardware runtime contract after AS5600 validation
- exact autoswitch -> source-restore ownership
- exact starter -> runtime truth mapping for stable payload/source tree in repo
- exact bridge interaction with future overlay/open-entry artifacts if those expand
