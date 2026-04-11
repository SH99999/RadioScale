# HANDOVER PACKAGE

## META
component: radio_scale
chat_origin: legacy Radio Scale / Scale FM development chat
date: 2026-04-11
baseline_id: radio_scale_baseline_1.10.2_resident_renderer
status_confidence: medium_low
authoritative: yes

## SCOPE
in_scope:
- radio-scale-service behavior as it affects the visible Radio Scale flow
- radio-scale-renderer / peppy integration
- station mapping
- marker logic / snap-to-station logic
- renderer state handling
- source tile / source open behavior
- metadata bridge toward the visible Radio Scale surface
- Display-/Overlay-Owner behavior from Radio Scale perspective
- Exit-, Hidden-, Visible- and Source-behavior
- current technical and UX bugs that directly affect Radio Scale
out_of_scope:
- new architecture beyond the current resident-renderer baseline
- new UX concepts beyond the current carried behavior
- fun_linea implementation details except shared overlay ownership impact
- analog autoswitch / Revox details except where they directly collide with Radio Scale
- 3-position switch plugin details
- frontpanel-engine work not directly consumed by Radio Scale
- historical reconstruction beyond explicit obsolete / abandoned markers below

## SOFTWARE SNAPSHOT
leading_version_build:
- Scale FM Overlay 1.10.2
- Scale FM Source 1.10.2
artifact_status:
- real installable zip artifacts were created
- 1.10.2 is the single leading baseline
- runtime validation of 1.10.2 on target hardware is not confirmed inside this chat
- earlier 1.9.x and 1.10.0/1.10.1 variants are not the baseline anymore
real_files_plugins_created:
- scale_fm_overlay_1.10.2.zip
- scale_fm_source_1.10.2.zip
- scale_fm_1.10.2_install_notes.txt
- scale_fm_1.10.2_feature_notes.txt
- scale_fm_overlay_1.10.2_release_notes.txt
- scale_fm_source_1.10.2_release_notes.txt
services_systemd_units:
- scale_fm_renderer.service
config_files:
- radio_scale_peppy_1.10.2/config.json
- radio_scale_peppy_1.10.2/UIConfig.json
- radio_scale_peppy_1.10.2/renderer/themes/braun_hd/theme.json
- radio_scale_source_1.10.2/config.json
assets:
- hiss audio wav files under radio_scale_peppy_1.10.2/audio/
- theme assets under radio_scale_peppy_1.10.2/renderer/themes/braun_hd/
install_order:
- install Scale FM Overlay 1.10.2
- install Scale FM Source 1.10.2
- reboot Volumio
runtime_entrypoints:
- source tile open path through radio_scale_source
- call methods:
  - gpio13OpenScale
  - encoder1ShortPress
  - encoder1LongPress
  - setScaleMode
  - setNormalMode
  - getControlStatus
- resident renderer service path remains scale_fm_renderer.service
- fallback classic spawn path must remain active if service is not running
dependencies:
- Volumio 4 / Bookworm
- Touch Display 3.6.0
- Rotary Encoder II 2.2.1
- Now Playing 1.0.6
- shared overlay owner marker file /tmp/mediastreamer_active_overlay.json
known_missing_pieces:
- 1.10.2 on-device validation status is missing
- exact runtime persistence file contract for last-station state is uncertain
- exact payload shape of getControlStatus is uncertain
- OE1 legacy cleanup remains incomplete

## FILE MANIFEST
- path: scale_fm_overlay_1.10.2.zip
  purpose: leading overlay plugin artifact
  status: authoritative
- path: scale_fm_source_1.10.2.zip
  purpose: leading source plugin artifact
  status: authoritative
- path: scale_fm_1.10.2_install_notes.txt
  purpose: install order, Rotary Encoder II mapping, exact websocket CALLMETHOD config, service notes
  status: authoritative
- path: scale_fm_1.10.2_feature_notes.txt
  purpose: leading renderer state model notes for idle / deep_idle / active
  status: authoritative
- path: scale_fm_overlay_1.10.2_release_notes.txt
  purpose: leading overlay release notes
  status: authoritative
- path: scale_fm_source_1.10.2_release_notes.txt
  purpose: leading source release notes
  status: authoritative
- path: radio_scale_peppy_1.10.2/index.js
  purpose: overlay plugin entry and public call methods
  status: authoritative
- path: radio_scale_peppy_1.10.2/renderer/radio_scale_renderer.py
  purpose: renderer runtime, visible/hidden/deep-idle behavior
  status: authoritative
- path: radio_scale_peppy_1.10.2/systemd/scale_fm_renderer.service
  purpose: resident renderer service unit shipped inside overlay package
  status: authoritative
- path: radio_scale_peppy_1.10.2/run_renderer_daemon.sh
  purpose: renderer daemon start path used by resident service
  status: authoritative
- path: radio_scale_peppy_1.10.2/renderer/themes/braun_hd/theme.json
  purpose: leading bundled theme configuration for layered radio scale
  status: authoritative
- path: radio_scale_source_1.10.2/index.js
  purpose: source tile / source open behavior for Scale FM
  status: authoritative
- path: scale_fm_overlay_1.10.1.zip
  purpose: previous resident-renderer iteration
  status: obsolete
- path: scale_fm_source_1.10.1.zip
  purpose: previous resident-renderer iteration
  status: obsolete
- path: scale_fm_overlay_1.9.x.zip family
  purpose: earlier safe/hotfix baseline family before current resident-renderer baseline
  status: obsolete
- path: scale_fm_source_1.9.x.zip family
  purpose: earlier safe/hotfix baseline family before current resident-renderer baseline
  status: obsolete
- path: radio_scale_peppy_1.5.x to 1.8.0 family
  purpose: older development lineage before Scale FM naming baseline
  status: obsolete

## KNOWLEDGE SNAPSHOT
current_purpose_of_component:
- Radio Scale is the visible radio-scale experience on top of Volumio, exposed through a Source tile and direct call-method entrypoints.
- It owns station mapping, marker/snap logic, renderer state transitions, hiss behavior, and the visible radio-scale surface.
- The current carried architecture is a resident renderer plus fallback spawn path.
stable_states:
- visible_active
- hidden_idle
- hidden_deep_idle
- source_open_request_received
- exit_to_regular_volumio_gui
stable_events:
- source tile open request
- gpio13OpenScale
- encoder1ShortPress
- encoder1LongPress
- setScaleMode
- setNormalMode
- getControlStatus
- shared overlay owner change via /tmp/mediastreamer_active_overlay.json
consumed_interfaces:
- Volumio browse/source open path via radio_scale_source
- Volumio plugin callMethod interface
- Rotary Encoder II websocket CALLMETHOD mapping
- Touch Display / Chromium visible GUI environment
- shared tmp file /tmp/mediastreamer_active_overlay.json
- current Volumio playback state for station restore behavior partially_working
produced_interfaces:
- visible Scale FM overlay surface
- public call methods listed above
- renderer service presence through scale_fm_renderer.service
- interaction side effects on playback / queue behavior partially_working
ownership_rules:
- owner scale_fm -> Radio Scale may render actively
- owner fun_linea -> Radio Scale must go to deep idle
- owner none -> Radio Scale uses normal hidden standby / idle path
assumptions:
- Volumio 4 / Bookworm is the target host
- Touch Display plugin is present and running
- Rotary Encoder II is the controlling input plugin for the mapped CALLMETHOD path
- Now Playing may be used as the post-exit visible landing surface
- exact persisted runtime file layout for last-station restore is uncertain
- exact metadata bridge payload shape is uncertain
decisions_that_must_survive_transition:
- keep public call methods unchanged:
  - gpio13OpenScale
  - encoder1ShortPress
  - encoder1LongPress
  - setScaleMode
  - setNormalMode
  - getControlStatus
- keep service name unchanged: scale_fm_renderer.service
- keep classic spawn fallback when service is not running
- respect /tmp/mediastreamer_active_overlay.json for owner arbitration
- hidden standby must stay deep-idle capable with near-zero CPU target
- visible mode must remain FPS-capped for Pi suitability
decisions_explicitly_abandoned:
- competing API renames for public call methods -> abandoned
- changing service path/name away from scale_fm_renderer.service -> abandoned
- removing fallback classic spawn path -> abandoned
- uncapped visible rendering as accepted behavior -> abandoned
- hidden draw-loop / full redraw in hidden state as accepted behavior -> abandoned
- older 1.9.x and 1.10.0/1.10.1 baselines as leading baseline -> obsolete

## STATUS SNAPSHOT
implemented:
- resident renderer baseline exists in the leading build
- service name retained as scale_fm_renderer.service
- fallback classic spawn path explicitly retained
- public call methods retained
- install notes provide exact Rotary Encoder II / websocket CALLMETHOD config
- shared overlay owner file is part of the intended 1.10.2 baseline
- hidden standby split into idle and deep_idle is part of the intended 1.10.2 baseline
- visible FPS cap is part of the intended 1.10.2 baseline
partially_working:
- startup time improved materially versus older builds; latest user-confirmed resident-renderer behavior reported around ~2 seconds in later testing before 1.10.2
- snap-to-station / marker lock behavior improved and was explicitly rated as good
- reopen on same / last station improved
- long-press exit cooperates with Now Playing and is considered useful
- hiss behavior is much improved versus early builds
- pointer movement improved but is still not fully liquid
- station start/stop behavior works but is still not fully consistent
broken:
- first start after boot can still show pointer moving to the beginning of the scale
- exit can still produce white flashes before regular Volumio GUI is fully back
- pointer still shows visible flicker / instability
- OE1 cleanup is incomplete in legacy lists / playlists / favorites
blocked:
- exact on-device runtime validation of the 1.10.2 baseline is blocked by absence of test feedback inside this chat
uncertain:
- exact runtime behavior of 1.10.2 on target Pi
- exact persisted file contract for last-station state
- exact produced payload of getControlStatus
- exact metadata bridge contract at payload level
known_bugs:
- first-show pointer hydration is not stable on first boot-time open
- white flash on exit still exists in tested resident-renderer lineage
- pointer jitter / anti-flicker still unresolved
- station start/stop behavior around selection remains not fully reproducible
- OE1 may persist in user-facing stored lists despite cleanup intent
regression_risks:
- changing call methods breaks encoder plugin mapping
- changing service path/name breaks current service install/runtime path
- removing fallback breaks open behavior when resident service is not up
- reintroducing hidden draw loop or uncapped render loop increases Pi load
- modifying exit path can reintroduce crash/flash/regression behavior
- modifying owner arbitration incorrectly can create overlay conflicts with fun_linea
do_not_change_list:
- gpio13OpenScale
- encoder1ShortPress
- encoder1LongPress
- setScaleMode
- setNormalMode
- getControlStatus
- scale_fm_renderer.service
- classic spawn fallback behavior
- shared owner file path /tmp/mediastreamer_active_overlay.json
next_smallest_integration_step:
- validate the 1.10.2 baseline on device specifically for hidden/deep_idle/owner behavior without changing public APIs
- then isolate only the remaining first-show pointer hydration, exit white flash, and pointer anti-flicker issues

## INTERFACE CONTRACT
incoming_events:
- source tile open request into radio_scale_source
- CALLMETHOD endpoint user_interface/radio_scale_peppy method gpio13OpenScale data ""
- CALLMETHOD endpoint user_interface/radio_scale_peppy method encoder1ShortPress data ""
- CALLMETHOD endpoint user_interface/radio_scale_peppy method encoder1LongPress data ""
- direct method calls for setScaleMode, setNormalMode, getControlStatus
- owner file changes in /tmp/mediastreamer_active_overlay.json
outgoing_events:
- visible overlay activation / deactivation on the display surface
- playback / queue side effects for last active station behavior partially_working
- getControlStatus response uncertain
state_inputs:
- current Volumio source/playback state partially_working
- saved last active station / pointer position uncertain
- shared owner marker /tmp/mediastreamer_active_overlay.json
- plugin config and theme config files
state_outputs:
- overlay visible / hidden / deep_idle state transitions
- resumed / restored last station behavior partially_working
- status response via getControlStatus uncertain
payload_shapes:
- CALLMETHOD payloads confirmed in install notes:
  - endpoint: user_interface/radio_scale_peppy
  - method: gpio13OpenScale | encoder1ShortPress | encoder1LongPress
  - data: ""
- payload shape of getControlStatus: uncertain
file_paths_used_at_runtime:
- /data/plugins/user_interface/radio_scale_peppy/index.js
- /data/plugins/user_interface/radio_scale_peppy/run_radio_scale.sh
- /data/plugins/user_interface/radio_scale_peppy/run_renderer_daemon.sh
- /data/plugins/user_interface/radio_scale_peppy/renderer/radio_scale_renderer.py
- /data/plugins/user_interface/radio_scale_peppy/renderer/themes/braun_hd/theme.json
- /data/plugins/music_service/radio_scale_source/index.js
- /etc/systemd/system/scale_fm_renderer.service
- /tmp/mediastreamer_active_overlay.json
shared_tmp_files:
- /tmp/mediastreamer_active_overlay.json
ports_urls_if_any:
- none authoritative
timeouts_retries:
- hidden runtime reload cadence is coarse in 1.10.2 design notes
- visible rendering is FPS-capped in 1.10.2 design notes
- exact timeout/retry numeric values are uncertain
fallback_behavior:
- if resident renderer service is not running, the classic spawn path must continue to work

## TEST / VALIDATION
what_was_tested:
- source tile open behavior across multiple releases
- encoder-triggered open / exit behavior
- snap-to-station behavior
- hiss behavior
- last-station reopen behavior
- resident renderer startup behavior in earlier 1.10.x feedback
- interaction with Now Playing on exit
what_passes:
- resident renderer direction improved startup versus older spawn-only behavior
- snap-on / station locking is materially improved and acceptable to the user in current lineage
- reopening after hiss-stop restoring the last active sender was explicitly rated good in later feedback
- long-press exit works and integrates acceptably with Now Playing
what_fails:
- first show after boot still has pointer-to-start sweep
- white flashes on exit remain
- pointer is still not fully stable / liquid
- OE1 cleanup still fails in legacy user lists
not_tested_yet:
- on-device runtime validation of 1.10.2 hidden idle / deep idle CPU behavior
- on-device validation of owner=fun_linea forcing deep idle in 1.10.2
- exact confirmation that 1.10.2 preserves all earlier partially_working startup/exit improvements
how_to_verify:
- install Overlay 1.10.2 first
- install Source 1.10.2 second
- reboot Volumio
- confirm service status with systemctl status scale_fm_renderer.service
- confirm encoder CALLMETHOD mapping exactly as documented in install notes
- test first open after boot
- test repeated open/close
- test exit while Now Playing is installed
- test owner marker transitions if fun_linea is present
logs_or_observations:
- first boot-time open has historically shown pointer sweep to scale start
- resident-renderer builds reduced startup materially but did not eliminate white-flash issues on exit
- pointer flicker / instability remains the main visible motion defect
- hidden/deep_idle in 1.10.2 is a documented build target, not yet a confirmed runtime result in this chat

## INTEGRATION NOTES
depends_on_other_components:
- Volumio source/browse system
- Touch Display plugin
- Rotary Encoder II
- Now Playing plugin for post-exit visual landing behavior
- fun_linea only through shared overlay ownership arbitration
affected_by_global_rules:
- public call methods must remain stable
- service path/name must remain stable
- fallback classic spawn path must remain
- shared tmp owner marker must be respected
known_conflicts:
- multiple competing encoder emits / overlapping control methods historically caused instability and crashes
- overlay conflicts are possible if owner arbitration is ignored
required_normalization_points:
- external naming should stay Scale FM Source / Scale FM Overlay
- internal plugin names remain radio_scale_source / radio_scale_peppy
- install order remains Overlay then Source then reboot
- encoder CALLMETHOD config must match install notes exactly

## MIGRATION INSTRUCTIONS FOR NEW CHAT
use_this_as_authoritative_baseline:
- yes
- use Scale FM Overlay 1.10.2 + Scale FM Source 1.10.2 + this handover as the single authoritative baseline
must_not_be_inferred_from_old_chat_history:
- do not resurrect older 1.9.x or 1.10.0/1.10.1 builds as current baseline
- do not rename public methods or service names based on older experiments
- do not invent unverified payload contracts or persistence paths
- do not mix unrelated frontpanel / autoswitch / fun_linea implementation detail into Radio Scale unless directly consumed by this baseline
safe_next_step:
- validate 1.10.2 exactly as built, without changing contracts, then narrow remaining work to first-show pointer hydration, exit white flash, and pointer anti-flicker
exact_questions_new_chat_should_answer:
- does 1.10.2 actually achieve deep idle with practically no draw work and near-zero CPU while hidden?
- does owner=fun_linea reliably force Radio Scale into deep idle?
- what exact file or state source is driving the first-show pointer-to-start sweep?
- what exact render/present step causes the exit white flashes?
- what minimal change stabilizes pointer flicker without changing snap behavior?
- where is OE1 still being sourced from in legacy stored lists?

## RAW OPEN PROBLEMS
- id: RS-OPEN-001
  symptom: first open after boot shows pointer traveling to the beginning of the scale
  likely_cause: initial state hydration / first-show sequencing loads fallback start position before valid saved state is applied
  affected_area: renderer state restore / startup sequencing
  severity: medium
  reproducibility: intermittent_but_reported_multiple_times
- id: RS-OPEN-002
  symptom: white flashes on overlay exit before regular Volumio GUI is fully back
  likely_cause: overlay hide / clear / Chromium repaint ordering
  affected_area: exit path / present path
  severity: medium
  reproducibility: reported_in_resident_renderer_lineage
- id: RS-OPEN-003
  symptom: pointer still flickers / jitters and is not fully liquid
  likely_cause: redraw/present instability and/or insufficient deadband/interpolation calmness
  affected_area: renderer motion path
  severity: medium
  reproducibility: consistent_user_report
- id: RS-OPEN-004
  symptom: station start/stop around selection is not fully reproducible
  likely_cause: partial state race between pointer position, lock state, and playback control
  affected_area: station mapping / marker logic / playback bridge
  severity: medium
  reproducibility: non_deterministic
- id: RS-OPEN-005
  symptom: OE1 remains in legacy lists / favorites / playlists
  likely_cause: cleanup is not removing already-persisted user data sources
  affected_area: seed / cleanup / persistence
  severity: low
  reproducibility: persistent_user_report
- id: RS-OPEN-006
  symptom: 1.10.2 deep idle / owner behavior is documented but not yet runtime-confirmed
  likely_cause: no on-device validation feedback yet for this exact build
  affected_area: hidden / deep_idle / owner arbitration
  severity: medium
  reproducibility: unknown

