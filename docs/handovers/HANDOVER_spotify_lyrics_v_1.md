# HANDOVER PACKAGE

## META
component: spotify_lyrics
chat_origin: legacy Altchat for RadioScale Overlay Bridge spotify/lyrics/cache branch; migrated on 2026-04-11
date: 2026-04-11
baseline_id: radioscale_overlay_bridge_0.2.3_db_cache_r1 | rollback_anchor=rsob_022sf22l.zip
status_confidence: medium
authoritative: yes

## SCOPE
in_scope:
- Spotify match logic as provider layer
- LRCLIB lyrics lookup as provider layer
- persistent cache / SQLite sidecar DB
- negative cache
- playlist dedupe / playlist presence cache
- metadata enrichment for Radio Scale and other consumers
- input/output fields of the spotify_lyrics component
- fallback behavior
- timeout / retry / backoff rules
- failure paths
- known weaknesses / uncertainties / API risks

out_of_scope:
- renderer ownership logic
- new renderer architecture
- new matching strategy beyond what is already implemented in the authoritative build
- new lyrics-provider strategy beyond what is already implemented in the authoritative build
- UI experiments from later 0.3.x releases
- broad historical narration
- speculative ownership/controller semantics not explicitly stabilized here
- Spotify redesign pending new API key

## SOFTWARE SNAPSHOT
leading_version_build:
- radioscale_overlay_bridge_0.2.3_db_cache_r1.zip
- package version inside zip: 0.2.3-db-cache-r1
- pretty name inside zip: RadioScale Overlay Bridge 0.2.3 DB Cache R1
- origin: conservative DB-cache branch built on top of approved rollback anchor rsob_022sf22l.zip

artifact_status:
- leading build for spotify_lyrics handover: authoritative
- rollback anchor: authoritative
- later UI-heavy 0.3.x line: experimental / non-authoritative for spotify_lyrics handover
- earlier 0.1.x recovery line: obsolete for future continuation

real_files_plugins_created:
- radioscale_overlay_bridge/package.json
- radioscale_overlay_bridge/index.js
- radioscale_overlay_bridge/db_cache.py
- radioscale_overlay_bridge/UIConfig.json
- radioscale_overlay_bridge/config.json
- radioscale_overlay_bridge/requiredConf.json
- radioscale_overlay_bridge/install.sh
- radioscale_overlay_bridge/uninstall.sh
- radioscale_overlay_bridge/public/index.html
- radioscale_overlay_bridge/public/app.js
- radioscale_overlay_bridge/public/style.css
- radioscale_overlay_bridge/i18n/strings_en.json
- README.md inside package
- release notes PDF for DB-cache branch
- user manual PDF for DB-cache branch

services_systemd_units:
- none
- runtime is owned by Volumio plugin lifecycle, not by a dedicated systemd unit

config_files:
- /data/configuration/user_interface/radioscale_overlay_bridge/config.json
- /data/configuration/user_interface/radioscale_overlay_bridge/requiredConf.json (package side)
- /data/configuration/user_interface/radioscale_overlay_bridge/spotify-auth.crt (runtime-generated)
- /data/configuration/user_interface/radioscale_overlay_bridge/spotify-auth.key (runtime-generated)
- /data/configuration/user_interface/radioscale_overlay_bridge/bridge_cache.sqlite (runtime-generated in DB branch)

assets:
- public/index.html
- public/app.js
- public/style.css
- no stable local artwork bundle
- artwork storage in DB branch is metadata / URL / thumbnail-reference only

install_order:
- rollback-safe base reference: rsob_022sf22l.zip
- current provider/cache branch: radioscale_overlay_bridge_0.2.3_db_cache_r1.zip
- do not continue from 0.3.x UI experiment zips for spotify_lyrics unless explicitly re-authorized

runtime_entrypoints:
- Volumio plugin lifecycle -> onStart -> startBridge() in index.js
- HTTP listener on configured port (default 5511)
- HTTPS listener on configured port (default 5443)
- polling loop against local Volumio state endpoint
- db_cache.py helper invoked as sidecar process for SQLite operations

dependencies:
- Node >=14
- Volumio >=4
- npm deps:
  - cors
  - express
  - kew
  - node-fetch
  - socket.io-client
  - v-conf
- runtime tools / stdlib:
  - python3
  - sqlite3 (stdlib via Python)
  - openssl
  - chown/chmod available on system

known_missing_pieces:
- lyrics sync was still only okish at rollback-anchor discussion point
- no Genius token / Genius fallback in authoritative line
- no stable multi-image artist gallery implementation
- no stable renderer-owned integration logic here
- Spotify changes were intentionally not further touched at one approved point because a new API key was awaited

## FILE MANIFEST
- path: rsob_022sf22l.zip
  purpose: authoritative rollback anchor / approved stable reference package before DB sidecar extension
  status: authoritative

- path: radioscale_overlay_bridge_0.2.3_db_cache_r1.zip
  purpose: authoritative spotify_lyrics DB-cache branch built on rollback anchor; leading handover build for this package
  status: authoritative

- path: RSOB_0.2.3_DB_Cache_R1_Release_Notes.pdf
  purpose: release notes for DB-cache branch
  status: authoritative

- path: RSOB_0.2.3_DB_Cache_R1_User_Manual.pdf
  purpose: user-facing manual for DB-cache branch
  status: authoritative

- path: radioscale_overlay_bridge_0.3.0.zip
  purpose: later UI/info-view expansion line; not baseline for spotify_lyrics migration
  status: experimental

- path: radioscale_overlay_bridge_0.3.1.zip
  purpose: later UI cleanup line; not baseline for spotify_lyrics migration
  status: experimental

- path: radioscale_overlay_bridge_0.3.2.zip
  purpose: later UI/duplicate-check iteration; not baseline for spotify_lyrics migration
  status: experimental

- path: radioscale_overlay_bridge_0.3.3.zip
  purpose: later UI/status-icon/rotation iteration; not baseline for spotify_lyrics migration
  status: experimental

- path: radioscale_overlay_bridge_0.1.0.zip .. radioscale_overlay_bridge_0.2.2.zip
  purpose: recovery / bring-up / stabilization chain leading toward rollback anchor; not authoritative continuation target now
  status: obsolete

## KNOWLEDGE SNAPSHOT
current_purpose_of_component:
- provider-layer bridge for:
  - normalized track metadata from Volumio / webradio
  - lyrics lookup via LRCLIB
  - Spotify track matching
  - playlist add with duplicate avoidance
  - persistent cache / negative cache / playlist presence cache
- component is not the renderer owner
- component is not the global controller of Radio Scale

stable_states:
- no_active_track
- normalized_track_available
- lyrics_disabled
- lyrics_plain_ready
- lyrics_synced_ready
- lyrics_negative_cache_hit
- spotify_not_connected
- spotify_connected_no_match_yet
- spotify_match_ready
- spotify_negative_cache_hit
- spotify_backoff_active
- playlist_slot_not_configured
- playlist_duplicate_detected
- persistent_cache_ready
- persistent_cache_disabled
- persistent_cache_helper_failed_but_online_path_continues

stable_events:
- poll_tick_5s
- volumio_state_polled
- track_changed
- normalized_track_changed
- fetch_lyrics_requested
- spotify_lookup_scheduled
- spotify_lookup_started
- spotify_lookup_rate_limited
- spotify_match_persisted
- lyrics_persisted
- negative_cache_written
- playlist_presence_hit
- add_to_playlist_requested
- add_to_playlist_duplicate
- add_to_playlist_success
- config_saved_and_bridge_restarted
- spotify_pkce_connect_requested
- spotify_callback_received

consumed_interfaces:
- local Volumio REST state:
  - GET http://127.0.0.1:3000/api/v1/getState
- Spotify Accounts / Web API:
  - authorize endpoint
  - token endpoint
  - /v1/me
  - /v1/search?type=track
  - /v1/playlists/{id}/tracks
- LRCLIB search API:
  - https://lrclib.net/api/search
- local Python sidecar:
  - db_cache.py via stdin/stdout JSON RPC-like action calls
- Volumio plugin config save callbacks

produced_interfaces:
- HTTP GET /api/state
- HTTP POST /api/lyrics/offset
- HTTP GET /api/spotify/auth/status
- HTTP GET /auth/start
- HTTPS GET /callback
- HTTP GET /api/spotify/match
- HTTP POST /api/spotify/add
- static UI from public/ via HTTP/HTTPS listeners
- Volumio settings UI sections via UIConfig.json

ownership_rules:
- component owns:
  - webradio metadata normalization for provider purposes
  - lyrics lookup/provider caching
  - Spotify matching/provider caching
  - negative cache
  - playlist dedupe cache
  - Spotify PKCE auth tokens for this plugin
- component does not own:
  - renderer layout decisions outside minimal provider UI
  - Radio Scale controller semantics
  - global ownership of playlist/source browsing in Volumio
  - speculative consumer-specific behavior unless explicitly connected later

assumptions:
- local Volumio state endpoint exists on port 3000
- publicHost is configured when HTTPS callback must be externally reachable
- openssl can generate local certificate if none exists
- Spotify access depends on configured client ID and valid user authorization
- LRCLIB remains the only authoritative lyrics provider in this line
- persistent DB cache is optional sidecar; if unavailable, baseline RAM/online path continues

decisions_that_must_survive_transition:
- treat Spotify + lyrics as provider layer, not controller layer
- authoritative rollback anchor is rsob_022sf22l.zip
- authoritative leading spotify_lyrics branch is radioscale_overlay_bridge_0.2.3_db_cache_r1.zip
- do not aggressively rewrite Spotify lookup strategy in this branch
- keep hard Spotify backoff behavior
- keep LRCLIB as authoritative lyrics provider in this line
- keep DB layer as additive sidecar, not invasive rewrite
- keep fixed 4 playlist slots
- use duplicate-check / playlist presence cache before adding when possible
- prefer polling-only mode in 0.2.3 DB branch for stability

decisions_explicitly_abandoned:
- continuing spotify_lyrics work from later 0.3.x UI experiment builds as baseline
- using Genius token / Genius fallback in authoritative line
- turning Spotify provider layer into renderer/controller owner
- relying on Volumio socket connector in 0.2.3 DB-cache branch
- JSON-file persistence as main cache backend for this branch

## STATUS SNAPSHOT
implemented:
- local state polling every 5000 ms from Volumio REST API
- webradio title parsing into artist/title using common separators
- normalization helpers:
  - diacritic stripping
  - DACH umlaut expansion / reverse expansion
  - title decoration stripping
  - artist variant expansion
- LRCLIB lyrics lookup
- plain + synced lyrics parsing
- in-memory lyrics cache
- in-memory Spotify match cache
- Spotify PKCE connect flow with local HTTPS callback
- Spotify hard backoff on 429
- 2-second scheduled Spotify lookup delay per track
- Spotify query variant generation and confidence scoring
- persistent SQLite sidecar cache branch with:
  - lyrics_cache table
  - spotify_match_cache table
  - negative_cache table
  - playlist_presence table
  - artwork_refs table
- DB helper fallback: if DB unavailable, component continues using RAM/online behavior
- playlist duplicate detection via cached presence + live playlist scan
- cache clear action for persistent cache branch

partially_working:
- lyrics sync quality was explicitly described as only okish at approved rollback-anchor point
- artwork enrichment exists only as metadata/URL reference storage, not as a rich stable multi-image experience
- playlist duplicate avoidance depends on Spotify read access and token scopes; not all device/runtime states were revalidated in this handover

broken:
- none declared as currently authoritative hard-broken in the handover baseline/branch itself
- treat any claims from later 0.3.x UI lines as non-authoritative for this component handover

blocked:
- further Spotify changes were explicitly deferred at one point pending a new API key / credential situation
- no approved migration here to a new lyrics provider beyond LRCLIB

uncertain:
- full on-device validation status of radioscale_overlay_bridge_0.2.3_db_cache_r1.zip is uncertain in this handover
- exact user-verified runtime behavior of DB branch after long-run use is uncertain
- whether playlist read scopes were re-authorized on the final device token after branch install is uncertain

known_bugs:
- lyrics sync not yet considered fully solved / final
- persistent cache branch device verification not fully captured in current visible chat state
- config version strings across older artifacts were historically inconsistent

regression_risks:
- touching Spotify query timing / backoff / matching thresholds
- replacing polling-only mode with socket-driven mode without explicit revalidation
- moving provider responsibilities into renderer/controller layer
- changing DB schema without migration / cleanup plan
- changing duplicate-check behavior without playlist read-scope verification

do_not_change_list:
- do not replace rsob_022sf22l.zip as rollback anchor without explicit new restore point
- do not rewrite Spotify strategy aggressively in this branch
- do not introduce Genius as implicit fallback without explicit approval
- do not infer renderer ownership logic
- do not use 0.3.x UI artifacts as spotify_lyrics baseline

next_smallest_integration_step:
- verify radioscale_overlay_bridge_0.2.3_db_cache_r1.zip on device against rollback anchor without changing Spotify strategy
- confirm bridge_cache.sqlite is created and reused after restart
- confirm duplicate-check + read-scope behavior on authorized Spotify token
- only then decide whether lyrics sync is the next isolated fix

## INTERFACE CONTRACT
incoming_events:
- poll_tick every 5000 ms
- Volumio state JSON from /api/v1/getState
- UI config save events:
  - configSaveService
  - configSaveTargets
  - configSaveLyrics
  - configSaveCache
  - configClearCaches
  - configSaveSpotify
  - spotifyConnectAction
  - spotifyDisconnectAction
  - configSavePlaylistSlotX
- browser/auth events:
  - GET /auth/start
  - GET /callback
- consumer actions:
  - POST /api/lyrics/offset
  - POST /api/spotify/add

outgoing_events:
- HTTP JSON responses
- HTTPS callback HTML success/failure page
- outgoing fetches to Spotify / LRCLIB
- outgoing helper process calls to db_cache.py
- Volumio toast messages on some user actions

state_inputs:
- from Volumio state JSON:
  - title
  - artist
  - service
  - stream
  - trackType
  - seek
  - status
  - albumart
- from plugin config:
  - port
  - httpsPort
  - publicHost
  - overlayWidthPercent
  - lyricsEnabled
  - preferSyncedLyrics
  - lyricsCacheTtlSeconds
  - lyricsSyncOffsetMs
  - spotifyClientId
  - spotifyScopes
  - playlistSlot{1..4}Enabled
  - playlistSlot{1..4}Name
  - playlistSlot{1..4}Id
  - persistentCacheEnabled
  - lyricsPersistentCacheDays
  - spotifyMatchCacheDays
  - negativeCacheHours
  - playlistPresenceCacheDays

state_outputs:
- /api/state payload includes:
  - ok
  - plugin
  - version
  - release
  - track
  - lyrics (+ offsetMs)
  - spotify.connected
  - spotify.userId
  - spotify.match
  - spotify.error
  - spotify.rateLimitedUntil
  - playlists[{slot,enabled,name,configured}]
  - runtime.{httpRunning,httpsRunning,httpError,httpsError,certReady,certError,persistentCacheEnabled,dbReady,dbPath,dbCounts}
  - lastUpdatedAt
- /api/spotify/auth/status payload includes:
  - connected
  - userId
  - redirectUri
  - authStartUrl
  - clientIdConfigured
  - error
  - rateLimitedUntil
- /api/spotify/add result payload includes:
  - ok
  - duplicate
  - added
  - playlist
  - track
  - artist
  - message
  - or error

payload_shapes:
- normalized track object:
  - key: lowercased "artist|title"
  - title
  - artist
  - station
  - service
  - albumart
  - status
  - trackType
- lyrics object:
  - mode: plain|synced
  - text
  - lines[] for synced mode
  - activeIndex
  - offsetMs added in output payload
- spotify match object:
  - ok
  - confidence
  - id
  - uri
  - title
  - artist
  - album
  - albumart
  - externalUrl
  - releaseDate

file_paths_used_at_runtime:
- /data/configuration/user_interface/radioscale_overlay_bridge/config.json
- /data/configuration/user_interface/radioscale_overlay_bridge/spotify-auth.crt
- /data/configuration/user_interface/radioscale_overlay_bridge/spotify-auth.key
- /data/configuration/user_interface/radioscale_overlay_bridge/bridge_cache.sqlite
- plugin helper path inside install: db_cache.py

shared_tmp_files:
- none explicitly stabilized in authoritative branch

ports_urls_if_any:
- local Volumio state source: http://127.0.0.1:3000/api/v1/getState
- plugin HTTP listener default: http://0.0.0.0:5511
- plugin HTTPS listener default: https://0.0.0.0:5443
- overlay URL derives from publicHost + port
- Spotify auth start URL derives from publicHost + httpsPort
- Spotify callback URL derives from publicHost + httpsPort + /callback
- LRCLIB search URL:
  - https://lrclib.net/api/search
- Spotify APIs:
  - https://accounts.spotify.com/authorize
  - https://accounts.spotify.com/api/token
  - https://api.spotify.com/v1/me
  - https://api.spotify.com/v1/search
  - https://api.spotify.com/v1/playlists/{id}/tracks

timeouts_retries:
- Volumio state poll interval: 5000 ms
- Volumio state fetch timeout: 5000 ms
- lyrics fetch timeout: 6000 ms
- Spotify token/search/general fetch timeout: 10000 ms
- pre-Spotify lookup delay after track change: 2000 ms
- lyrics active-index timer: 400 ms
- Spotify hard backoff on HTTP 429:
  - use Retry-After when present
  - else 30 seconds fallback
- in-memory Spotify match cache TTL: 10 minutes
- in-memory lyrics cache TTL: lyricsCacheTtlSeconds (default 21600 sec)
- persistent DB TTL defaults:
  - lyricsPersistentCacheDays: 14
  - spotifyMatchCacheDays: 45
  - negativeCacheHours: 6
  - playlistPresenceCacheDays: 120

fallback_behavior:
- if track is webradio, attempt to split title into artist/title using separators
- if no split succeeds, keep raw title and fallback artist/station fields
- lyrics resolution order:
  1. RAM lyrics cache
  2. persistent SQLite lyrics cache (if enabled and ready)
  3. negative cache check
  4. LRCLIB online lookup
- Spotify match resolution order:
  1. RAM Spotify match cache
  2. persistent SQLite Spotify match cache (if enabled and ready)
  3. negative cache check
  4. Spotify online lookup after 2-second schedule delay
- if SQLite sidecar fails:
  - continue with baseline RAM + online path
- if HTTPS cert generation fails:
  - HTTPS listener remains down; HTTP listener may still run
- if Spotify 429 occurs:
  - set hard backoff and block further Spotify requests until backoff expires

## TEST / VALIDATION
what_was_tested:
- rollback anchor rsob_022sf22l.zip was explicitly described by user as current okish reference except lyrics sync; Spotify intentionally left untouched there pending new API key
- authoritative DB branch artifact was built and documented
- package structure exists in artifact
- DB helper file exists in artifact
- package metadata/config/runtime files exist in artifact

what_passes:
- artifact contains expected sidecar-cache files
- rollback anchor contains established provider logic
- branch clearly preserves baseline-safe intent in README and package metadata

what_fails:
- none conclusively device-verified as failing in this authoritative handover beyond the explicit lyrics-sync quality issue inherited from baseline context

not_tested_yet:
- full on-device runtime verification of radioscale_overlay_bridge_0.2.3_db_cache_r1.zip
- restart persistence behavior of sqlite branch on real device
- long-run duplicate-check behavior after token refreshes
- interaction between persistent cache and delayed Spotify lookups under real station churn

how_to_verify:
- install radioscale_overlay_bridge_0.2.3_db_cache_r1.zip on device
- confirm plugin starts and listeners behave as expected
- confirm /data/configuration/user_interface/radioscale_overlay_bridge/bridge_cache.sqlite is created
- play a repeated song twice across restart and check whether lyrics/match return faster from cache
- verify no excessive Spotify queries during repeated metadata churn
- verify duplicate add is prevented when track already exists in configured playlist
- verify rollback by reinstalling rsob_022sf22l.zip and deleting bridge_cache.sqlite if needed

logs_or_observations:
- 0.2.3 branch logs explicitly state: Volumio socket connector disabled; polling-only mode used for stability
- baseline discussion explicitly confirmed Spotify hard backoff behavior was present
- baseline discussion explicitly confirmed LRCLIB was the lyrics provider and Genius token was not used

## INTEGRATION NOTES
depends_on_other_components:
- Volumio core state endpoint on port 3000
- Radio Scale / Fun Mode / other consumers only as external consumers of provider output
- Spotify Web API + Accounts service
- LRCLIB provider
- local Python runtime for DB sidecar helper
- openssl for local certificate generation

affected_by_global_rules:
- provider-layer only; do not infer renderer/controller ownership
- maintain explicit rollback anchor
- conservative changes only
- keep documentation / restore path explicit

known_conflicts:
- port conflicts on 5511 or 5443
- missing / stale publicHost causing callback reachability issues
- missing or stale Spotify scopes/token may break playlist read or duplicate detection
- absence of openssl breaks HTTPS callback listener
- disabling persistent cache or sidecar failures drop branch back to RAM-only behavior

required_normalization_points:
- webradio title parsing via separators: ` - `, ` – `, ` — `, ` | `, ` ~ `, `: `
- normalize strings with NFKD + diacritic stripping + apostrophe cleanup
- German variant expansion: ä/ae, ö/oe, ü/ue, ß/ss
- title decoration stripping (live/remaster/edit/etc.)
- playlist ID normalization from URL/URI/raw input

## MIGRATION INSTRUCTIONS FOR NEW CHAT
use_this_as_authoritative_baseline:
- yes: radioscale_overlay_bridge_0.2.3_db_cache_r1.zip for spotify_lyrics continuation
- rollback anchor: rsob_022sf22l.zip

must_not_be_inferred_from_old_chat_history:
- do not infer that 0.3.x UI builds are the current spotify_lyrics baseline
- do not infer Genius fallback exists
- do not infer persistent cache existed in rollback anchor; it did not
- do not infer renderer ownership or controller ownership from unrelated UI experiments
- do not infer Spotify strategy changes beyond the conservative branch documented here

safe_next_step:
- verify 0.2.3 DB-cache branch on actual device against rollback anchor without changing Spotify strategy
- keep focus strictly on provider/cache validation first
- if validation passes, isolate lyrics-sync improvements as separate next step

exact_questions_new_chat_should_answer:
- Does radioscale_overlay_bridge_0.2.3_db_cache_r1.zip run cleanly on device without regressions versus rsob_022sf22l.zip?
- Is bridge_cache.sqlite created and reused correctly across restart?
- Are persistent lyrics hits and Spotify match hits observable after restart?
- Does duplicate detection prevent repeated adds without reintroducing Spotify request spam?
- Is lyrics sync still the smallest unresolved issue after DB-branch validation?

## RAW OPEN PROBLEMS
- id: OPR-001
  symptom: lyrics sync quality is not final / was only described as okish
  likely_cause: viewport/sync behavior unresolved at baseline discussion point; exact root cause not stabilized here
  affected_area: synced lyrics presentation / timing
  severity: medium
  reproducibility: repeatable according to prior discussion context

- id: OPR-002
  symptom: Spotify should not be further changed in this line until new API key / credential situation is resolved
  likely_cause: external credential / API constraint
  affected_area: Spotify provider evolution
  severity: medium
  reproducibility: persistent policy constraint, not a runtime bug

- id: OPR-003
  symptom: DB-cache branch is built and documented but complete device verification state is uncertain in this handover
  likely_cause: context gap / no authoritative final field validation captured here
  affected_area: persistent cache branch readiness
  severity: medium
  reproducibility: always relevant until verified

- id: OPR-004
  symptom: older artifact versions have inconsistent internal version strings
  likely_cause: iterative release churn
  affected_area: artifact traceability / release hygiene
  severity: low
  reproducibility: present in historical artifacts

