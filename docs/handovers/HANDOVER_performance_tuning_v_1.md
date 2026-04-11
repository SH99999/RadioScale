# HANDOVER PACKAGE

## META
component: performance_tuning
chat_origin: MediaStreamer startup / appliance / boot-runtime altchat
date: 2026-04-11
baseline_id: bootdelay_fix_v0.1.0__plus__mediastreamer_hybrid_startup_standby_v0.2.2_stable
status_confidence: high_for_baseline__medium_for_nonbaseline_runtime_details
authoritative: yes

## SCOPE
in_scope:
- boot behavior as observed and stabilized in this chat
- service order around boot / kiosk / display runtime
- Chromium / kiosk / display runtime only where system-relevant
- black/white/reload sequences as observed in tests
- stable startup baseline selection
- runtime control states actually carried by the stable hybrid line
- measured / observed boot timing, regression criteria, runtime risks
- strict separation of stable baseline vs nonleading variants

out_of_scope:
- any new development
- any new optimization
- any new architecture
- any new UX
- any new problem solving
- any historical narrative beyond status labeling
- treating experimental startup/appliance/direct-now-playing variants as active baseline
- claiming solved hidden-state deep idle / visible FPS cap / render-throttling when not stabilized in this chat

## SOFTWARE SNAPSHOT
leading_version_build:
- mediastreamer_bootdelay_fix_v0.1.0
- mediastreamer_hybrid_startup_standby_v0.2.2_stable

artifact_status:
- active_baseline: authoritative
- mediastreamer_hybrid_startup_standby_v0.2.1: partial
- all appliance / direct-now-playing / launcher / keeper / topmost-keeper / patch lines: experimental or abandoned

real_files_plugins_created:
- /opt/mediastreamer-bootdelay-fix
- /opt/mediastreamer-hybrid
- /opt/mediastreamer-hybrid-install
- /opt/mediastreamer-hybrid/server.py
- /opt/mediastreamer-hybrid/kiosk-wrapper.sh
- /opt/mediastreamer-hybrid/state/state.json
- /opt/mediastreamer-hybrid/www/
- /etc/systemd/system/mediastreamer-hybrid.service
- /etc/systemd/system/volumio-kiosk.service.d/10-mediastreamer-hybrid.conf
- /usr/local/bin/mediastreamer-shellctl

services_systemd_units:
- mediastreamer-hybrid.service
- volumio-kiosk.service with drop-in override only

config_files:
- /boot/cmdline.txt
- /etc/systemd/system/mediastreamer-hybrid.service
- /etc/systemd/system/volumio-kiosk.service.d/10-mediastreamer-hybrid.conf
- /opt/mediastreamer-hybrid/state/state.json

assets:
- stable hybrid web assets exist under /opt/mediastreamer-hybrid/www/
- exact stable asset inventory: uncertain
- appliance_artwork.png and later artwork/keeper assets belong to nonleading variants

install_order:
- mediastreamer_bootdelay_fix_v0.1.0
- mediastreamer_hybrid_startup_standby_v0.2.1
- mediastreamer_hybrid_startup_standby_v0.2.2_stable over v0.2.1
- do not layer experimental startup/appliance/direct-now-playing releases onto the authoritative baseline

runtime_entrypoints:
- volumio-kiosk.service -> /opt/mediastreamer-hybrid/kiosk-wrapper.sh
- mediastreamer-hybrid.service -> /opt/mediastreamer-hybrid/server.py
- /usr/local/bin/mediastreamer-shellctl

dependencies:
- Volumio 4
- touch_display plugin / volumio-kiosk.service path
- Chromium kiosk runtime
- local Volumio UI on 127.0.0.1:3000
- local Now Playing plugin on 127.0.0.1:4004
- Raspberry Pi 4B
- 14.1" HDMI IPS touch panel 1920x550
- HiFiBerry DAC+ ADC Pro

known_missing_pieces:
- authoritative hidden-state deep idle implementation in this chat
- authoritative visible-state FPS cap implementation in this chat
- authoritative render-throttling implementation in this chat
- visually appliance-like seamless startup from first visible frame to Now Playing
- exact authoritative stable asset list for v0.2.2 stable

## FILE MANIFEST
- path: /boot/cmdline.txt
  purpose: bootdelay token; authoritative stable baseline uses bootdelay=0
  status: authoritative

- path: /opt/mediastreamer-bootdelay-fix
  purpose: install root for stable bootdelay optimization
  status: authoritative

- path: /opt/mediastreamer-hybrid
  purpose: install root for stable hybrid startup/standby runtime
  status: authoritative

- path: /opt/mediastreamer-hybrid/server.py
  purpose: hybrid state API / startup state handling
  status: authoritative

- path: /opt/mediastreamer-hybrid/kiosk-wrapper.sh
  purpose: kiosk wrapper used by stable hybrid runtime
  status: authoritative

- path: /opt/mediastreamer-hybrid/state/state.json
  purpose: persisted runtime state for standby / startup flags / version
  status: authoritative

- path: /opt/mediastreamer-hybrid/www
  purpose: stable startup shell web content
  status: partial

- path: /etc/systemd/system/mediastreamer-hybrid.service
  purpose: systemd unit for hybrid runtime server
  status: authoritative

- path: /etc/systemd/system/volumio-kiosk.service.d/10-mediastreamer-hybrid.conf
  purpose: volumio-kiosk drop-in redirecting startup through hybrid wrapper
  status: authoritative

- path: /usr/local/bin/mediastreamer-shellctl
  purpose: runtime control interface for standby / wake / status
  status: authoritative

- path: /opt/mediastreamer-appliance-finish-install
  purpose: appliance experiment install root
  status: experimental

- path: /opt/mediastreamer-direct-now-playing-install
  purpose: direct-now-playing experiment install root
  status: experimental

- path: /opt/mediastreamer-direct-now-playing-launcher-install
  purpose: launcher experiment install root
  status: experimental

- path: /opt/mediastreamer-direct-now-playing-keeper-install
  purpose: keeper experiment install root
  status: experimental

- path: /opt/mediastreamer-direct-now-playing-topmost-keeper-install
  purpose: topmost-keeper experiment install root
  status: experimental

- path: /opt/mediastreamer-direct-now-playing-topmost-keeper-patch-install
  purpose: topmost-keeper patch experiment install root
  status: experimental

## KNOWLEDGE SNAPSHOT
current_purpose_of_component:
- stable startup/runtime glue for Volumio kiosk boot path
- provide bootdelay optimization plus stable hybrid startup/standby
- preserve standby/wake/status runtime control
- prefer Now Playing handover without replacing the underlying Volumio/touch_display kiosk chain

stable_states:
- hidden:
  - technical_definition: state.standby == true
  - source_confidence: authoritative_for_hybrid_control_only
- idle:
  - technical_definition: uncertain
  - source_confidence: uncertain
- visible:
  - technical_definition: state.standby == false
  - source_confidence: authoritative_for_hybrid_control_only
- transition:
  - technical_definition: startup phase before final handover completes; represented by startup_completed false until handover is completed
  - source_confidence: authoritative_for_hybrid_control_only

stable_events:
- mediastreamer-shellctl standby
- mediastreamer-shellctl wake
- mediastreamer-shellctl status
- startup handover to preferred target URL
- fallback from 4004 to 3000 if preferred target unavailable

consumed_interfaces:
- volumio-kiosk.service start path
- touch_display-managed kiosk runtime
- local HTTP reachability of 127.0.0.1:4004 and 127.0.0.1:3000
- /boot/cmdline.txt bootdelay token

produced_interfaces:
- mediastreamer-shellctl CLI
- hybrid state API via mediastreamer-hybrid.service
- stable hybrid startup handover path for volumio-kiosk.service drop-in

ownership_rules:
- bootdelay fix owns only bootdelay optimization
- hybrid runtime owns startup wrapper behavior and standby/wake/status state
- touch_display and volumio-kiosk.service remain the underlying kiosk mechanism in the leading baseline
- experimental startup/appliance variants do not own the authoritative runtime baseline

assumptions:
- preferred target is 127.0.0.1:4004 when reachable
- fallback target is 127.0.0.1:3000 when 4004 is unavailable
- stable baseline remains layered over Volumio/touch_display rather than replacing it
- visual appliance perfection was not achieved in the authoritative baseline

decisions_that_must_survive_transition:
- exactly one authoritative baseline:
  - mediastreamer_bootdelay_fix_v0.1.0
  - mediastreamer_hybrid_startup_standby_v0.2.2_stable
- v0.2.1 is not the leading baseline
- all startup/appliance/direct-now-playing variants after v0.2.2 are nonleading
- no further startup architecture should be inferred from this chat
- preferred handover order must remain 4004 then 3000 for the leading baseline
- functional stability outranks visual appliance polish in the chosen baseline

decisions_explicitly_abandoned:
- using v0.2.3 appliance stable as active baseline
- using v0.2.4 appliance finish as active baseline
- using v0.3.0 direct-now-playing as active baseline
- using v0.3.1 launcher as active baseline
- using v0.3.2 keeper as active baseline
- using v0.3.3 topmost-keeper as active baseline
- using v0.3.4 patch as active baseline
- Chromium GPU-disable experiment as accepted fix
- continued patching of the Volumio/X/Chromium visual handover path as economical path to final appliance startup

## STATUS SNAPSHOT
implemented:
- bootdelay=0 stable optimization
- stable hybrid startup wrapper
- mediastreamer-hybrid.service in the stable line
- volumio-kiosk drop-in to route startup through hybrid wrapper
- standby/wake/status control via mediastreamer-shellctl
- preferred handover to 4004 with fallback to 3000
- functional startup path to Now Playing in the authoritative stable line

partially_working:
- v0.2.1 hybrid baseline before 0.2.2 stable handover correction
- experimental appliance/direct-now-playing lines improved visual continuity but remained nonleading
- startup visuals on the authoritative baseline are functional but not appliance-final

broken:
- seamless appliance-grade direct startup from first visible frame to Now Playing in the experimented lines
- elimination of black/white/reload sequence in experimented launcher/keeper/topmost-keeper lines

blocked:
- authoritative claim that hidden-state deep idle is implemented here
- authoritative claim that visible-state FPS cap is implemented here
- authoritative claim that render-throttling is implemented here
- perfect visual continuity inside the Volumio -> X -> openbox -> Chromium -> plugin chain

uncertain:
- exact stable asset inventory for v0.2.2 stable
- exact stable baseline timing constants directly isolated from v0.2.2-only verify
- whether any runtime throttling exists in the stable hybrid web layer
- whether hidden/idle distinction exists beyond standby true/false in the stable line

known_bugs:
- leading stable baseline is functionally stable but visually not fully appliance-like
- experimental lines repeatedly showed black/white/reload transitions
- patch layering in experimental lines produced version-string mismatches across state / shellctl / local health

regression_risks:
- touching volumio-kiosk.service runtime path
- touching touch_display-managed startup behavior
- reintroducing experimental appliance/direct-now-playing layers over the authoritative baseline
- further Chromium flag experiments without isolated rollback
- assuming /tmp ready-marker handshake logic is production-ready

do_not_change_list:
- bootdelay_fix_v0.1.0 as authoritative boot baseline
- hybrid_v0.2.2_stable as authoritative runtime baseline
- target preference order 4004 then 3000
- mediastreamer-shellctl standby/wake/status contract
- classification of all post-0.2.2 startup/appliance variants as nonleading
- no inferred deep-idle / FPS cap / throttling implementation from this chat

next_smallest_integration_step:
- in the new performance_tuning chat, normalize all runtime/performance extraction to the authoritative baseline only:
  - mediastreamer_bootdelay_fix_v0.1.0
  - mediastreamer_hybrid_startup_standby_v0.2.2_stable

## INTERFACE CONTRACT
incoming_events:
- system boot reaching volumio-kiosk.service path
- mediastreamer-shellctl standby
- mediastreamer-shellctl wake
- mediastreamer-shellctl status
- local availability of 4004 and 3000 during startup handover

outgoing_events:
- updates to state.json
- handover to 4004 when available
- fallback handover to 3000 when 4004 unavailable
- standby/wake transitions

state_inputs:
- standby command
- wake command
- boot/startup event
- availability of target URLs

state_outputs:
- standby: boolean
- startup_completed: boolean
- startup_started_at: integer|null
- last_transition: integer|null
- version: string

payload_shapes:
- state.json:
  - standby: boolean
  - startup_completed: boolean
  - startup_started_at: integer|null
  - last_transition: integer|null
  - version: string

file_paths_used_at_runtime:
- /boot/cmdline.txt
- /opt/mediastreamer-hybrid/server.py
- /opt/mediastreamer-hybrid/kiosk-wrapper.sh
- /opt/mediastreamer-hybrid/state/state.json
- /etc/systemd/system/mediastreamer-hybrid.service
- /etc/systemd/system/volumio-kiosk.service.d/10-mediastreamer-hybrid.conf
- /usr/local/bin/mediastreamer-shellctl

shared_tmp_files:
- leading_baseline: none authoritative
- experimental_only:
  - /tmp/mediastreamer-kiosk-ready
  - /tmp/mediastreamer-artwork-keeper.pid
  - /tmp/mediastreamer-artwork-keeper.ready

ports_urls_if_any:
- preferred_target: http://127.0.0.1:4004/
- fallback_target: http://127.0.0.1:3000/
- local_state_api_port_in_hybrid_line: uncertain

timeouts_retries:
- stable-derived hybrid verify values observed in-chat:
  - minStartupMs: 7000
  - fallbackToVolumioAfterMs: 22000
- direct v0.2.2-only authoritative isolation: uncertain
- experimental lines changed timing values; ignore for leading baseline

fallback_behavior:
- try 4004 first
- if 4004 unavailable, fall back to 3000
- no authoritative further fallback behavior from this chat

## TEST / VALIDATION
what_was_tested:
- repeated boots on Raspberry Pi 4B / Volumio 4 / 1920x550 panel
- systemd-analyze boot timing
- journalctl on volumio-kiosk.service and volumio service
- hybrid service status and state transitions
- mediastreamer-shellctl standby/wake/status
- local reachability of 4004 and 3000
- multiple install / uninstall / rollback cycles across stable and nonleading startup variants

what_passes:
- bootdelay=0 optimization
- stable hybrid startup runtime
- mediastreamer-shellctl standby/wake/status on the stable line
- 4004 preferred handover with 3000 fallback on the stable line
- functional startup to Now Playing on the leading stable baseline

what_fails:
- visually seamless appliance-grade startup in nonleading lines
- full elimination of black/white/reload sequences in nonleading lines
- authoritative stabilization of direct-now-playing startup chain

not_tested_yet:
- no further authoritative testing after startup track closure beyond extraction
- no authoritative stable-line deep-idle validation
- no authoritative stable-line FPS-cap validation
- no authoritative stable-line render-throttling validation

how_to_verify:
- systemd-analyze
- journalctl -u volumio-kiosk.service -b --no-pager
- journalctl -u volumio -b --no-pager
- mediastreamer-shellctl standby
- mediastreamer-shellctl wake
- mediastreamer-shellctl status
- confirm active install roots correspond to the leading baseline only
- confirm target preference reaches 4004 first and 3000 only as fallback

logs_or_observations:
- repeated startup timings observed around roughly 24–25.6 seconds to graphical target
- repeated MPD boot behavior observed:
  - Output device has changed, restarting MPD
- nonleading lines repeatedly showed visual sequences including:
  - schwarz - backlight - mediastreamer - schwarz - weiß - mediastreamer - now playing
  - backlight - mediastreamer - schwarz - weiß - mediastreamer - play now
- leading stable baseline was accepted as functionally stable despite nonfinal visuals

## INTEGRATION NOTES
depends_on_other_components:
- Volumio core
- touch_display
- volumio-kiosk.service
- Now Playing plugin on 4004
- Volumio UI on 3000
- MPD / audio-init sequence during boot

affected_by_global_rules:
- startup/appliance track was explicitly frozen and archived
- only the declared stable baseline remains active
- all later startup variants are reference evidence only

known_conflicts:
- layering later appliance/direct-now-playing packages over the stable baseline caused confusion and inconsistent version/state reporting
- older experimental systemd drop-ins could remain unless cleaned
- trying to perfect visuals in the current Volumio/X/Chromium chain produced diminishing returns

required_normalization_points:
- normalize all future performance work to:
  - mediastreamer_bootdelay_fix_v0.1.0
  - mediastreamer_hybrid_startup_standby_v0.2.2_stable
- ignore experimental install roots and drop-ins when establishing runtime truth
- treat /tmp ready-marker and artwork-keeper files as experimental only

## MIGRATION INSTRUCTIONS FOR NEW CHAT
use_this_as_authoritative_baseline:
- mediastreamer_bootdelay_fix_v0.1.0
- mediastreamer_hybrid_startup_standby_v0.2.2_stable

must_not_be_inferred_from_old_chat_history:
- do not infer that any post-0.2.2 startup/appliance release is stable
- do not infer that hidden-state deep idle was implemented here
- do not infer that visible-state FPS cap was implemented here
- do not infer that render-throttling was implemented here
- do not infer that appliance-like startup was achieved
- do not infer that GPU-disable Chromium flags helped
- do not infer that direct-now-playing line should be used as active runtime base

safe_next_step:
- in the new Performance Tuning chat, extract runtime/performance behavior only from the authoritative baseline and treat all other variants as obsolete evidence or experimental failures

exact_questions_new_chat_should_answer:
- which runtime/performance properties are actually implemented on bootdelay_fix_v0.1.0 + hybrid_v0.2.2_stable
- what is the authoritative service sequence on the leading baseline
- which boot/runtime regressions must block changes on the leading baseline
- how should hidden / idle / visible / transition be measured on the leading baseline without importing abandoned startup experiments

## RAW OPEN PROBLEMS
- id: stable_startup_not_appliance_final
  symptom: leading stable baseline is functional but visually not fully appliance-like
  likely_cause: visible transitions remain inherent in the Volumio -> X -> openbox -> Chromium chain
  affected_area: boot visuals / kiosk first-paint path
  severity: medium
  reproducibility: high

- id: hidden_idle_definition_incomplete
  symptom: hidden and idle are not fully distinguished beyond standby=true/false in the authoritative baseline
  likely_cause: this chat did not stabilize a deeper idle architecture on the leading baseline
  affected_area: hidden/idle runtime semantics
  severity: medium
  reproducibility: high

- id: fps_cap_not_authoritatively_present
  symptom: no authoritative extracted implementation of visible-state FPS cap in the leading baseline
  likely_cause: performance-control features were not stabilized in this chat
  affected_area: visible runtime rendering policy
  severity: medium
  reproducibility: high

- id: render_throttling_not_authoritatively_present
  symptom: no authoritative extracted implementation of render-throttling in the leading baseline
  likely_cause: startup/runtime stabilization took precedence over render-policy work
  affected_area: rendering runtime policy
  severity: medium
  reproducibility: high

- id: experimental_variants_not_reusable_as_baseline
  symptom: later startup/appliance variants contain useful evidence but cannot be reused as authoritative runtime baseline
  likely_cause: unresolved black/white/keeper/launcher issues and patch layering complexity
  affected_area: startup experiment line
  severity: medium
  reproducibility: high

