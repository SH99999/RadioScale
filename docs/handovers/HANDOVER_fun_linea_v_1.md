# HANDOVER PACKAGE

## META
component: fun_linea
chat_origin: legacy MediaStreamer Fun Linea delivery / runtime / plugin iteration chat
date: 2026-04-11
baseline_id: FL_BASELINE_0_4_2_RUNTIME_VALIDATED
status_confidence: medium
authoritative: yes

## SCOPE
in_scope:
- fun_linea runtime behavior on Volumio 4
- overlay rendering behavior
- open / close / encoder / GPIO handler behavior
- interaction with Radio Scale / Scale FM renderer
- audio stability constraints
- standby / visible / hidden behavior
- actor runtime direction for Dog Line as first production actor
- plugin packaging state across produced builds
- known config-page failures and packaging failures
- boundaries for future work in new specialized chat
out_of_scope:
- new architecture invention
- new UX invention
- new actor families beyond already discussed scope
- new performance experiments outside validated baseline
- retrospective narrative
- speculative ownership systems not already used
- claims of fully working importer / catalog system
- claims of fully working multi-actor production engine

## SOFTWARE SNAPSHOT
leading_version_build: fun_linea 0.4.2
artifact_status: leading validated runtime baseline; later builds exist but are not authoritative
real_files_plugins_created:
- fun_linea_overlay_0.4.2.zip
- fun_linea_source_0.4.2.zip
- fun_linea_0.4.2_docs.zip
- fun_linea_0.4.2_full_bundle.zip
- later non-authoritative builds: 0.5.0, 0.6.0 bundles
services_systemd_units:
- none authoritative for fun_linea in leading baseline
- shared coordination relies on runtime / tmp markers, not on a required always-on fun_linea service in the validated baseline
config_files:
- overlay plugin config exists in produced builds but config-menu behavior has repeatedly failed in practice
- source plugin config exists in produced builds but config-menu behavior has repeatedly failed in practice
- config handling must be treated as broken until revalidated
assets:
- authoritative runtime baseline does not depend on validated SVG / pose packs
- Dog Line visual asset direction exists only as later partial work, not yet authoritative
install_order:
- install overlay plugin first
- install source plugin second
- reboot Pi
runtime_entrypoints:
- browser tile open via source plugin
- GPIO / encoder open via overlay plugin method gpio13OpenFun
- encoder1ShortPress open path
- encoder1LongPress close / return path
dependencies:
- Volumio 4
- Chromium / kiosk environment already used by system
- existing MediaStreamer overlay environment
- coexistence with Scale FM / Radio Scale overlay runtime
known_missing_pieces:
- validated working plugin config pages
- validated importer / catalog workflow
- validated production-ready Dog Line asset runtime
- validated overlay/full-stage dynamic asset switching using new visual packs

## FILE MANIFEST
- path: fun_linea_overlay_0.4.2.zip
  purpose: validated runtime baseline overlay plugin with stable open/close/audio coexistence behavior
  status: authoritative
- path: fun_linea_source_0.4.2.zip
  purpose: validated runtime baseline source plugin paired with overlay 0.4.2
  status: authoritative
- path: fun_linea_0.4.2_docs.zip
  purpose: supporting notes bundle for 0.4.2 baseline
  status: authoritative
- path: fun_linea_0.4.2_full_bundle.zip
  purpose: authoritative full bundle for runtime baseline handoff
  status: authoritative
- path: fun_linea_overlay_0.5.0.zip
  purpose: experimental config/importer attempt
  status: obsolete
- path: fun_linea_source_0.5.0.zip
  purpose: experimental config/importer attempt
  status: obsolete
- path: fun_linea_dog_line_pack_01.zip
  purpose: attempted starter content pack delivered with 0.5.0 line
  status: partial
- path: fun_linea_overlay_0.6.0.zip
  purpose: first Dog Line production-pass attempt using pose / visual asset direction
  status: partial
- path: fun_linea_source_0.6.0.zip
  purpose: paired source plugin for 0.6.0 attempt
  status: partial
- path: fun_linea_dog_line_visual_pack_01.zip
  purpose: later Dog Line visual asset pack
  status: partial
- path: Fun_Linea_Transfer_2026-04-11.docx
  purpose: previous broad transfer document for new chat seeding
  status: partial
- path: Mediastreamer_Fun_Mode_Uebergabe.docx
  purpose: authoritative creative / fun-mode conceptual source for figure logic and overlay intent
  status: authoritative

## KNOWLEDGE SNAPSHOT
current_purpose_of_component:
- fun_linea is an overlay / experience layer for MediaStreamer, not a core playback system
- it must be able to run as a localized overlay over existing GUI / radio scale and also support a larger full-stage / screensaver-like presentation when explicitly active
- it must coexist with Radio Scale / Scale FM and must not destabilize radio playback, MPD, DAC, or the kiosk GUI
stable_states:
- closed / inactive
- visible / opened by tile or GPIO / encoder
- hidden idle coordinated with Scale FM in validated 0.4.2 behavior
stable_events:
- browser tile open
- gpio13OpenFun
- encoder1ShortPress
- encoder1LongPress
consumed_interfaces:
- Volumio plugin method invocation from Rotary Encoder II / plugin UI
- existing overlay environment / Chromium kiosk
- shared temp marker for active overlay ownership coordination
produced_interfaces:
- overlay open / close behavior
- visible overlay rendering when active
- release bundles and docs
ownership_rules:
- authoritative behavior is coordination through shared tmp ownership marker and active pausing of competing heavy renderer behavior
- validated baseline used a shared file: /tmp/mediastreamer_active_overlay.json
- when Fun Linea becomes active, Scale FM must not continue heavy active rendering at the same time
- do not invent a larger global ownership model beyond the above validated coordination file behavior
assumptions:
- Fun Linea is not allowed to become an always-on heavy renderer while hidden
- overlay / experience layer status is preserved
- core player ownership remains outside fun_linea
- future actors / loops should be additive and content-pack oriented, but this is not yet validated as implemented
- plugin config pages are not trustworthy until revalidated
decisions_that_must_survive_transition:
- 0.4.2 is the single leading runtime baseline
- audio stability and coexistence with Radio Scale are more important than new visuals
- Fun Linea remains overlay / experience layer, not core system
- hidden standby must behave as deep idle, not active redraw
- never allow two heavy renderers to run actively together
- preserve encoder / GPIO open-close contract
- preserve ability to support both overlay mode and full-stage mode dynamically
- Dog Line is the first chosen production actor
- visual future should use pose / asset / vector logic rather than primitive live-drawn doodle logic
decisions_explicitly_abandoned:
- treating earlier config/importer builds as working
- treating primitive parametric doodle output as acceptable final visual direction
- treating always-on resident fun_linea rendering as acceptable
- treating early 0.3.x / 0.4.0 / 0.5.0 config-page behavior as recoverable without explicit revalidation

## STATUS SNAPSHOT
implemented:
- plugin pair exists: overlay + source
- open via browser tile works in validated baseline
- open / close via encoder / GPIO works in validated baseline
- shared runtime coordination with Radio Scale / Scale FM was validated in 0.4.2
- radio playback can remain stable while fun_linea opens in 0.4.2
- active overlay ownership file path was used in runtime coordination
partially_working:
- later Dog Line visual / asset direction in 0.6.0
- later pose / pack based visual path
- plugin config files physically exist in multiple later builds
- overlay vs full-stage concept is established conceptually but not fully validated on later visual builds
broken:
- plugin configuration pages have repeatedly shown "Konfiguration nicht verfügbar" or crashed
- importer / catalog behavior is not validated and must not be assumed working
- several later releases broke open paths, config pages, or uninstall paths
- 0.5.0 config/importer attempt is not a safe baseline
blocked:
- production use of Dog Line visual packs is blocked by lack of validated config/runtime integration on later builds
- future actor catalog workflow is blocked by unvalidated importer/config UI path
uncertain:
- 0.6.0 practical runtime stability on target Pi
- working state of 0.6.0 config pages
- exact completeness of later asset manifests at runtime
known_bugs:
- repeated Volumio config page failure: "Konfiguration nicht verfügbar"
- earlier uninstall failure in one build: TypeError removeServiceEnableFlag is not a function
- earlier builds caused audio device busy or slow-motion audio due to renderer CPU starvation
- later visual builds may not preserve stable runtime unless revalidated
regression_risks:
- reintroducing heavy hidden renderer loops
- reintroducing ALSA / audio initialization in renderer path
- breaking GPIO / encoder contracts
- breaking shared ownership coordination with Scale FM
- shipping importer/config UI changes without runtime validation
- swapping to new visual engine without preserving 0.4.2 handler logic
do_not_change_list:
- open path contract: gpio13OpenFun / encoder1ShortPress
- close path contract: encoder1LongPress
- overlay / experience-layer status of component
- shared active overlay coordination concept using tmp ownership file
- no-ALSA / no-MPD interference requirement
- audio stability priority over visuals
next_smallest_integration_step:
- preserve 0.4.2 runtime/handler behavior exactly
- build one revalidated Dog Line visual engine pass on top of that
- keep only Dog Line in scope
- restore actually working config pages only if they are needed and tested
- do not reintroduce importer until config/runtime path is proven

## INTERFACE CONTRACT
incoming_events:
- browser tile open via source plugin
- endpoint user_interface/fun_linea_overlay method gpio13OpenFun data ""
- endpoint user_interface/fun_linea_overlay method encoder1ShortPress data ""
- endpoint user_interface/fun_linea_overlay method encoder1LongPress data ""
outgoing_events:
- visible overlay presentation
- close / return behavior to existing GUI flow
- runtime coordination writes to shared tmp ownership file
state_inputs:
- current active overlay ownership state from shared tmp file
- plugin runtime state / settings files in local plugin runtime paths (exact later build details uncertain)
- kiosk / GUI visibility environment
state_outputs:
- active / inactive overlay state
- ownership marker updates
- local renderer runtime markers in plugin runtime path (exact later build coverage uncertain)
payload_shapes:
- Rotary Encoder II open call payload shape:
  {"endpoint":"user_interface/fun_linea_overlay","method":"gpio13OpenFun","data":""}
- short press open payload shape:
  {"endpoint":"user_interface/fun_linea_overlay","method":"encoder1ShortPress","data":""}
- long press close payload shape:
  {"endpoint":"user_interface/fun_linea_overlay","method":"encoder1LongPress","data":""}
file_paths_used_at_runtime:
- /tmp/mediastreamer_active_overlay.json
- plugin-local runtime files existed in multiple builds but exact authoritative local file list beyond the tmp ownership file is uncertain in this handover and must not be inferred
shared_tmp_files:
- /tmp/mediastreamer_active_overlay.json
ports_urls_if_any:
- none authoritative for fun_linea itself
- Chromium / kiosk environment exists globally in system, but no new authoritative fun_linea-specific port contract is declared here
timeouts_retries:
- no authoritative numeric timeout contract preserved from this chat
fallback_behavior:
- if Fun Linea is not active, it must not consume heavy render resources
- if Scale FM is active, Fun Linea must not attempt to become a second heavy active renderer without ownership transition
- fallback behavior for importer/config paths is not authoritative because those paths are not validated

## TEST / VALIDATION
what_was_tested:
- install / open / close across multiple iterations
- radio playback coexistence while opening fun_linea
- encoder / GPIO opening paths
- practical effect of renderer coordination on audio stability
- top / ps observation of heavy CPU contention in broken builds
what_passes:
- on 0.4.2 baseline: radio runs, remains stable, fun_linea opens, radio continues cleanly
- open / close path via browser and encoder is validated on 0.4.2 baseline
what_fails:
- multiple config-page attempts across later builds
- several earlier builds with audio busy or slow-motion due to heavy renderer contention
- importer / catalog workflow not validated
not_tested_yet:
- practical validation of 0.6.0 Dog Line production-pass artifacts
- stable full-stage dynamic visuals using later asset packs
- reliable config UI on later builds
how_to_verify:
- install overlay then source then reboot
- verify radio / web radio playback stays stable before opening fun_linea
- open via browser tile and via GPIO / encoder
- close via encoder1LongPress
- confirm no audio slowdown and no extra CPU-heavy hidden renderer remains active
- inspect process list and top if audio degrades
logs_or_observations:
- broken state was previously confirmed by ps/top showing radio_scale_renderer.py and fun_linea_renderer.py both consuming very high CPU simultaneously
- validated fix direction in 0.4.2 reduced conflict enough that radio remained stable while fun_linea opened

## INTEGRATION NOTES
depends_on_other_components:
- Radio Scale / Scale FM runtime behavior
- Volumio plugin framework
- Rotary Encoder II mapping behavior
- global Chromium / kiosk environment
affected_by_global_rules:
- audio output / MPD / DAC stability constraints
- overlay ownership coordination with other renderers
- hidden standby must stay light
known_conflicts:
- heavy concurrent rendering with Scale FM
- plugin config menu failures in Volumio
- later feature attempts that modified runtime or importer behavior without practical validation
required_normalization_points:
- normalize all future work to 0.4.2 runtime baseline before adding visual engine changes
- normalize visual direction to vector / pose / asset approach
- normalize component role as overlay / experience layer
- normalize config path only after explicit validation

## MIGRATION INSTRUCTIONS FOR NEW CHAT
use_this_as_authoritative_baseline:
- yes: use FL_BASELINE_0_4_2_RUNTIME_VALIDATED as single leading baseline
must_not_be_inferred_from_old_chat_history:
- do not infer that later builds are more correct just because they are newer
- do not infer working config menus from presence of config files
- do not infer working importer / catalog flow
- do not infer global ownership model beyond shared tmp coordination already used
- do not infer that all discussed actors are implemented
safe_next_step:
- preserve 0.4.2 runtime / audio / ownership behavior exactly
- implement a single revalidated Dog Line visual runtime layer on top
- keep configuration surface minimal until it is proven working
exact_questions_new_chat_should_answer:
- what exact files and runtime code from 0.4.2 must be preserved unchanged to keep audio stable?
- can Dog Line visual assets be integrated without touching the validated ownership / handler path?
- what is the smallest working config surface that can be reintroduced and actually validated in Volumio?
- how should overlay mode and full-stage mode be switched while preserving the same runtime contracts?
- what is the minimal asset / pose pack contract for future actors after Dog Line is validated?

## RAW OPEN PROBLEMS
- id: OP-001
  symptom: plugin config pages frequently show "Konfiguration nicht verfügbar"
  likely_cause: Volumio config loading / UI config flow broken in multiple builds
  affected_area: plugin configuration UI
  severity: high
  reproducibility: high
- id: OP-002
  symptom: later builds exist but are not validated on target Pi
  likely_cause: build-only verification without practical runtime validation
  affected_area: later visual runtime line (0.6.0 and related)
  severity: medium
  reproducibility: high
- id: OP-003
  symptom: concurrent heavy renderer activity caused audio slowdown / instability in broken states
  likely_cause: both fun_linea and radio_scale heavy render loops active simultaneously while hidden/visible
  affected_area: runtime performance, audio stability
  severity: critical
  reproducibility: previously high before 0.4.2 direction
- id: OP-004
  symptom: Dog Line visual direction not yet validated in runtime despite asset attempts
  likely_cause: visual engine transition incomplete
  affected_area: actor model / animation engine
  severity: medium
  reproducibility: high
- id: OP-005
  symptom: importer / catalog concept discussed but not safe to rely on
  likely_cause: no validated end-to-end runtime + config implementation
  affected_area: future asset extensibility
  severity: medium
  reproducibility: high

