# HANDOVER PACKAGE

## META
component: revox_autoswitch
chat_origin: mediastreamer_volumio4_revox_adc_autoswitch_track
date: 2026-04-11
baseline_id: revox_autoswitch_baseline_v2_receiver_style_threshold_logic
status_confidence: medium
authoritative: yes

## SCOPE
in_scope:
- ALSA-based signal detection via arecord + sox amplitude sampling
- threshold-based activation logic
- debounce via confirmation counters
- asymmetric start/stop delay logic
- ADC routing via amixer (HiFiBerry DAC+ ADC Pro)
- systemd service lifecycle management
- tape monitor toggle behavior

out_of_scope:
- native Volumio source tile integration
- renderer implementation
- radio_scale_source plugin logic
- frontpanel encoder binding
- metadata rendering
- previous-source restore persistence logic
- snd-aloop loopback architecture

## SOFTWARE SNAPSHOT
leading_version_build: revox_autoswitch_v2_asymmetric_delay_logic
artifact_status: scripts_created_and_deployed_runtime_confirmed
real_files_plugins_created:
- /home/volumio/tape_monitor.sh
- /home/volumio/revox_autoswitch.sh
- /etc/systemd/system/revox-autoswitch.service
services_systemd_units:
- revox-autoswitch.service
config_files:
- none_persistent_outside_scripts
assets:
- none
install_order:
1_copy_scripts
2_set_execute_permissions
3_copy_systemd_service
4_daemon_reload
5_enable_service
6_start_service
runtime_entrypoints:
- systemd -> revox-autoswitch.service
- manual_toggle -> tape_monitor.sh

dependencies:
- arecord
- sox
- bc
- amixer

known_missing_pieces:
- previous_source_restore
- explicit_renderer_state_signal
- GUI_source_visibility

## FILE MANIFEST
- path: /home/volumio/tape_monitor.sh
  purpose: toggle_ADC_input_routing
  status: authoritative

- path: /home/volumio/revox_autoswitch.sh
  purpose: amplitude_threshold_monitor_loop
  status: authoritative

- path: /etc/systemd/system/revox-autoswitch.service
  purpose: persistent_background_runtime_controller
  status: authoritative

- path: /etc/mpd.conf
  purpose: attempted_input_injection
  status: abandoned

- path: snd_aloop_kernel_module
  purpose: ALSA_loopback_strategy
  status: abandoned

## KNOWLEDGE SNAPSHOT
current_purpose_of_component:
provide_receiver_style_tape_monitor_behavior_without_volumio_premium

stable_states:
- tape_monitor_enabled
- tape_monitor_disabled

stable_events:
- amplitude_above_threshold
- amplitude_below_threshold_confirmed

consumed_interfaces:
- ALSA_capture_device_hw4
- systemd_service_runtime

produced_interfaces:
- ADC_input_route_state
- volumio_stop_command

ownership_rules:
ADC_routing_control_owned_by_tape_monitor_sh
signal_detection_owned_by_revox_autoswitch_sh

assumptions:
ADC_card_index_equals_4
VINL1_and_VINR1_available_as_valid_inputs
sox_available_runtime


decisions_that_must_survive_transition:
- do_not_modify_ADC_routing_method
- maintain_threshold_detection_architecture
- maintain_systemd_execution_model


decisions_explicitly_abandoned:
- snd_aloop_detection_path
- mpd_input_block_strategy
- legacy_hifiberry_adc_plugin_strategy

## STATUS SNAPSHOT
implemented:
- amplitude_threshold_detection_loop
- asymmetric_start_stop_delay
- ADC_input_routing_toggle
- systemd_service_autostart

partially_working:
- automatic_return_behavior_after_signal_loss

broken:
- none_confirmed

blocked:
- native_volumio_source_tile_creation

uncertain:
- interaction_with_renderer_overlay_state
- interaction_with_future_source_restore_logic

known_bugs:
- possible_device_busy_if_capture_locked_by_other_process

regression_risks:
- changing_card_index
- altering_threshold_without_measurement


do_not_change_list:
- ADC_control_names
- VINL1_assignment
- VINR1_assignment


next_smallest_integration_step:
expose_runtime_state_flag_for_renderer_overlay_indicator

## INTERFACE CONTRACT
incoming_events:
- amplitude_sampling_cycle

outgoing_events:
- ADC_route_enable
- ADC_route_disable

state_inputs:
- amplitude_value

state_outputs:
- tape_monitor_state_flag

payload_shapes:
amplitude_float_scalar

file_paths_used_at_runtime:
- /home/volumio/tape_monitor.sh
- /home/volumio/revox_autoswitch.sh

shared_tmp_files:
- none_defined

ports_urls_if_any:
- none

timeouts_retries:
poll_interval_1_second
stop_confirm_cycles_4

fallback_behavior:
manual_toggle_available_via_script

## TEST / VALIDATION
what_was_tested:
- script_execution
- systemd_start
- ADC_route_toggle

what_passes:
- routing_activation
- routing_deactivation

what_fails:
- none_confirmed

not_tested_yet:
- long_duration_runtime_stability

how_to_verify:
systemctl_status_revox_autoswitch
amixer_ADC_input_readback

logs_or_observations:
journalctl_service_output_available

## INTEGRATION NOTES
depends_on_other_components:
- ALSA
- volumio_runtime_environment

affected_by_global_rules:
no_modification_of_volumio_core_allowed

known_conflicts:
possible_capture_device_lock

required_normalization_points:
card_index_detection_if_hardware_changes

## MIGRATION INSTRUCTIONS FOR NEW CHAT
use_this_as_authoritative_baseline:
yes

must_not_be_inferred_from_old_chat_history:
legacy_detection_paths
experimental_loopback_designs

safe_next_step:
export_runtime_state_flag_for_overlay

exact_questions_new_chat_should_answer:
- how_to_surface_tape_state_to_renderer

## RAW OPEN PROBLEMS
- id: RP01
  symptom: device_busy_error_possible
  likely_cause: concurrent_capture_access
  affected_area: signal_detection
  severity: medium
  reproducibility: intermittent

