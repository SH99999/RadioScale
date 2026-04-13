# SKILL — OVERLAY COMPONENT GOVERNANCE V1

## Purpose
This skill helps agents work on components that share display/runtime space with other overlays.

## Leading rule
Treat overlay behavior as governance-critical, not just UI detail.

## Required overlay questions
- what opens the overlay?
- what renders or maintains the overlay?
- is there a separate launcher artifact?
- is there a separate runtime artifact?
- what file or state indicates active overlay control?
- what happens when another overlay becomes active?
- what is the hidden or deep-idle behavior?
- what must rollback remove or unregister?

## Bridge-specific note
Bridge is already governed as an overlay component.
Any Bridge change should preserve:
- clean-replace deployment semantics
- repo-driven deployment
- rollback plus Volumio unregistration when applicable
- explicit overlay-control documentation

## Documentation expectations
Overlay components should document:
- launcher artifact role
- runtime artifact role
- overlay-control behavior
- visible vs hidden behavior
- known interaction with other overlays
