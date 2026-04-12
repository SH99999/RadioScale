# HARDWARE CONFIG CONTRACT V2

Status: authoritative integration standard.

## Purpose

This contract extends the hardware baseline so future buttons, replacement input devices and hardware-facing plugins can be integrated without silent GPIO conflicts.

## Leading rule

No component chat may independently redefine GPIO ownership, input mappings, or hardware-critical pin usage.
All hardware-touching changes must conform to the normalized hardware allocation model below.

## Current authoritative assignments

### Rotary Encoder II validated mappings

Encoder 0:
- pinA: GPIO 5
- pinB: GPIO 6
- push: GPIO 13

Encoder 1:
- pinA: GPIO 17
- pinB: GPIO 27
- push: GPIO 22

## Allocation model

Each GPIO relevant to this project must be treated as one of these states:
- `assigned_runtime`
- `reserved_planned`
- `unassigned`
- `forbidden`

Only `assigned_runtime` values are authoritative live mappings.
`reserved_planned` values may be documented for future hardware features but must not be used by component chats until promoted to `assigned_runtime` by integration decision.

## Hardware branch rule

Hardware-facing development belongs on:
- `dev/hardware`

This branch is used for:
- AS5600 integration
- replacement encoder plugins
- input abstraction changes
- additional button integration
- future frontpanel hardware adaptation

## Safety rule

No hardware-facing change may silently conflict with:
- current encoder mappings
- HiFiBerry DAC+ ADC Pro usage
- already-normalized runtime assignments

## Additional button rule

Future buttons are allowed only through this lifecycle:
1. proposed in hardware branch
2. marked as `reserved_planned`
3. conflict-reviewed in integration
4. promoted to `assigned_runtime`
5. consumed by a component after promotion

## Non-goal

This contract does not assign speculative GPIOs for yet-unvalidated hardware features.
Unknown future assignments remain intentionally open until explicitly normalized.
