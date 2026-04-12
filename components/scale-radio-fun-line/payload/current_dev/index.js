"use strict";

const libQ = require('kew');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const vConf = require('v-conf');
const io = require('socket.io-client');

const PUBLIC_OVERLAY_NAME = 'Fun Linea Overlay';
const PUBLIC_SOURCE_LABEL = 'Fun Linea';

module.exports = ControllerFunLineaOverlay;

function ControllerFunLineaOverlay(context) {
  this.context = context;
  this.commandRouter = context.coreCommand;
  this.logger = context.logger;
  this.configManager = context.configManager;
  this.config = new vConf();
  this.pluginDir = __dirname;
  this.runtimeDir = path.join(this.pluginDir, 'runtime');
  this.statePath = path.join(this.runtimeDir, 'state.json');
  this.settingsPath = path.join(this.runtimeDir, 'settings.json');
  this.rendererReadyPath = path.join(this.runtimeDir, 'renderer_ready.json');
  this.rendererPidPath = path.join(this.runtimeDir, 'renderer.pid');
  this.serviceEnableFlagPath = path.join(this.runtimeDir, 'service_enabled.flag');
  this.sharedActiveOverlayPath = '/tmp/mediastreamer_active_overlay.json';
  this.scaleRuntimeDir = '/data/plugins/user_interface/radio_scale_peppy/runtime';
  this.scaleRendererPidPath = path.join(this.scaleRuntimeDir, 'renderer.pid');
  this.rendererProcess = null;
  this.rendererOwnedByPlugin = false;
  this.rendererRetryTimer = null;
  this.pollTimer = null;
  this.lastStateDigest = '';
  this.overlayVisible = false;
  this.lastVolumioState = this.buildIdleState();
  this.rendererShutdownRequested = false;
}

ControllerFunLineaOverlay.prototype.onVolumioStart = function () {
  const configFile = this.commandRouter.pluginManager.getConfigurationFile(this.context, 'config.json');
  this.config = new vConf();
  this.config.loadFile(configFile);
  return libQ.resolve();
};

ControllerFunLineaOverlay.prototype.onStart = function () {
  const defer = libQ.defer();
  Promise.resolve()
    .then(() => {
      this.logger.info('[fun_linea_overlay] onStart');
      this.ensureRuntimeDir();
      this.overlayVisible = false;
      this.releaseActiveOverlay('fun_linea');
      this.resumeScaleRendererIfPaused();
      this.writeServiceEnableFlag();
      this.writeStateIfChanged(this.buildRendererState(this.lastVolumioState));
      this.writeSettingsFile();
      this.startPolling();
      this.logger.info('[fun_linea_overlay] renderer enabled = ' + JSON.stringify(this.isRendererEnabled()));
      if (this.isResidentRendererServiceEnabled()) {
        this.logger.info('[fun_linea_overlay] resident renderer service mode active - expecting systemd-managed preload');
      } else if (this.shouldPreloadResidentRenderer()) {
        this.scheduleResidentRendererStart(1000);
      } else {
        this.logger.info('[fun_linea_overlay] renderer waiting for tile or GPIO trigger');
      }
      defer.resolve();
    })
    .catch((err) => {
      this.logger.error('[fun_linea_overlay] onStart failed: ' + err.stack);
      defer.reject(err);
    });
  return defer.promise;
};

ControllerFunLineaOverlay.prototype.onStop = function () {
  try {
    this.overlayVisible = false;
    this.releaseActiveOverlay('fun_linea');
    this.resumeScaleRendererIfPaused();
    this.removeServiceEnableFlag();
    this.writeSettingsFile();
    this.stopPolling();
    this.clearRendererRetryTimer();
    this.rendererShutdownRequested = true;
    this.stopRenderer();
    return libQ.resolve();
  } catch (err) {
    this.logger.error('[fun_linea_overlay] onStop failed: ' + err.stack);
    return libQ.reject(err);
  }
};

ControllerFunLineaOverlay.prototype.getConfigurationFiles = function () {
  return ['config.json'];
};

ControllerFunLineaOverlay.prototype.getConfigValue = function (key, fallback) {
  const raw = this.config.get(key);
  if (raw && typeof raw === 'object' && Object.prototype.hasOwnProperty.call(raw, 'value')) {
    return raw.value;
  }
  return typeof raw === 'undefined' ? fallback : raw;
};

ControllerFunLineaOverlay.prototype.getBooleanConfig = function (key, fallback) {
  const value = this.getConfigValue(key, fallback);
  if (typeof value === 'boolean') return value;
  if (typeof value === 'number') return value !== 0;
  if (typeof value === 'string') {
    const lower = value.trim().toLowerCase();
    if (['true', '1', 'yes', 'on'].includes(lower)) return true;
    if (['false', '0', 'no', 'off', ''].includes(lower)) return false;
  }
  return Boolean(value);
};

ControllerFunLineaOverlay.prototype.getNumberConfig = function (key, fallback) {
  const parsed = Number(this.getConfigValue(key, fallback));
  return Number.isFinite(parsed) ? parsed : Number(fallback);
};

ControllerFunLineaOverlay.prototype.getStringConfig = function (key, fallback) {
  const value = this.getConfigValue(key, fallback);
  return (value === null || typeof value === 'undefined') ? String(fallback || '') : String(value);
};

ControllerFunLineaOverlay.prototype.setConfigValue = function (key, value) {
  const raw = this.config.get(key);
  if (raw && typeof raw === 'object' && Object.prototype.hasOwnProperty.call(raw, 'value')) {
    raw.value = value;
    this.config.set(key, raw);
  } else {
    this.config.set(key, value);
  }
};

ControllerFunLineaOverlay.prototype.writeServiceEnableFlag = function () {
  this.ensureRuntimeDir();
  if (!this.isResidentRendererServiceEnabled()) {
    this.removeServiceEnableFlag();
    return;
  }
  try {
    fs.writeFileSync(this.serviceEnableFlagPath, JSON.stringify({ enabled: true, ts: Date.now() }, null, 2));
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] writeServiceEnableFlag failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.removeServiceEnableFlag = function () {
  try {
    if (fs.existsSync(this.serviceEnableFlagPath)) {
      fs.unlinkSync(this.serviceEnableFlagPath);
    }
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] removeServiceEnableFlag failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.readJsonFileSafe = function (filePath, fallback) {
  try {
    if (!fs.existsSync(filePath)) return fallback;
    const raw = String(fs.readFileSync(filePath, 'utf8') || '').trim();
    if (!raw) return fallback;
    return JSON.parse(raw);
  } catch (err) {
    return fallback;
  }
};

ControllerFunLineaOverlay.prototype.setActiveOverlay = function (owner) {
  try {
    fs.writeFileSync(this.sharedActiveOverlayPath, JSON.stringify({ owner: String(owner || 'none'), ts: Date.now() }, null, 2));
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] setActiveOverlay failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.releaseActiveOverlay = function (owner) {
  try {
    if (!fs.existsSync(this.sharedActiveOverlayPath)) return;
    const current = this.readJsonFileSafe(this.sharedActiveOverlayPath, {});
    const currentOwner = String((current && current.owner) || 'none');
    if (!owner || currentOwner === String(owner)) {
      fs.writeFileSync(this.sharedActiveOverlayPath, JSON.stringify({ owner: 'none', ts: Date.now() }, null, 2));
    }
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] releaseActiveOverlay failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.getScaleRendererPid = function () {
  try {
    if (!fs.existsSync(this.scaleRendererPidPath)) return null;
    const raw = String(fs.readFileSync(this.scaleRendererPidPath, 'utf8') || '').trim();
    const pid = Number(raw);
    return Number.isInteger(pid) && pid > 1 ? pid : null;
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] getScaleRendererPid failed: ' + err.message);
    return null;
  }
};

ControllerFunLineaOverlay.prototype.pauseScaleRendererIfRunning = function () {
  const pid = this.getScaleRendererPid();
  if (!pid) return;
  try {
    process.kill(pid, 0);
    process.kill(pid, 'SIGSTOP');
    this.logger.info('[fun_linea_overlay] SIGSTOP sent to Scale FM renderer pid=' + pid);
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] pauseScaleRendererIfRunning failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.resumeScaleRendererIfPaused = function () {
  const pid = this.getScaleRendererPid();
  if (!pid) return;
  try {
    process.kill(pid, 0);
    process.kill(pid, 'SIGCONT');
    this.logger.info('[fun_linea_overlay] SIGCONT sent to Scale FM renderer pid=' + pid);
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] resumeScaleRendererIfPaused failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.ensureRuntimeDir = function () {
  fs.mkdirSync(this.runtimeDir, { recursive: true });
};

ControllerFunLineaOverlay.prototype.delay = function (ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

ControllerFunLineaOverlay.prototype.clearRendererReadyFlag = function () {
  try {
    if (fs.existsSync(this.rendererReadyPath)) {
      fs.unlinkSync(this.rendererReadyPath);
    }
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] clearRendererReadyFlag failed: ' + err.message);
  }
};

ControllerFunLineaOverlay.prototype.isRendererReady = function () {
  try {
    if (!fs.existsSync(this.rendererReadyPath)) {
      return false;
    }
    const raw = fs.readFileSync(this.rendererReadyPath, 'utf8');
    const parsed = raw && raw.trim() ? JSON.parse(raw) : null;
    return Boolean(parsed && parsed.ready);
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] isRendererReady failed: ' + err.message);
    return false;
  }
};

ControllerFunLineaOverlay.prototype.waitForRendererReadyBriefly = function (timeoutMs) {
  const deadline = Date.now() + Math.max(0, Number(timeoutMs) || 0);
  const poll = () => {
    if (this.isRendererReady()) {
      return Promise.resolve({ success: true, ready: true });
    }
    if (Date.now() >= deadline) {
      return Promise.resolve({ success: true, ready: false, timeout: true });
    }
    return this.delay(40).then(poll);
  };
  return poll();
};

ControllerFunLineaOverlay.prototype.buildIdleState = function () {
  return {
    status: 'stop',
    service: '',
    title: 'Fun Linea',
    artist: 'La Linea Engine',
    album: '',
    albumart: '',
    uri: '',
    duration: 0,
    seek: 0,
    samplerate: '',
    bitdepth: '',
    channels: '',
    trackType: '',
    updatedAt: Date.now(),
    animationPulse: 0,
    ui_mode: this.overlayVisible ? 'fun' : 'normal'
  };
};

ControllerFunLineaOverlay.prototype.buildRendererState = function (rawState) {
  const state = rawState && typeof rawState === 'object' ? rawState : {};
  const status = String(state.status || 'stop');
  const seekMs = Number(state.seek || 0);
  const pulseHz = status === 'play' ? 3.9 : 1.2;
  const pulse = 0.5 + 0.5 * Math.sin((Date.now() / 1000) * pulseHz);
  return {
    status,
    service: String(state.service || ''),
    title: String(state.title || state.name || 'Fun Linea'),
    artist: String(state.artist || ''),
    album: String(state.album || ''),
    albumart: String(state.albumart || ''),
    uri: String(state.uri || ''),
    duration: Number(state.duration || 0),
    seek: seekMs,
    samplerate: String(state.samplerate || ''),
    bitdepth: String(state.bitdepth || ''),
    channels: String(state.channels || ''),
    trackType: String(state.trackType || ''),
    updatedAt: Date.now(),
    animationPulse: pulse,
    ui_mode: this.overlayVisible ? 'fun' : 'normal'
  };
};

ControllerFunLineaOverlay.prototype.writeJsonFile = function (filePath, payload) {
  fs.writeFileSync(filePath, JSON.stringify(payload, null, 2));
};

ControllerFunLineaOverlay.prototype.writeStateIfChanged = function (payload) {
  const digest = JSON.stringify(payload || {});
  if (digest === this.lastStateDigest) {
    return false;
  }
  this.lastStateDigest = digest;
  this.writeJsonFile(this.statePath, payload || this.buildIdleState());
  return true;
};

ControllerFunLineaOverlay.prototype.writeSettingsFile = function () {
  const payload = {
    visible: Boolean(this.overlayVisible),
    ui_mode: this.overlayVisible ? 'fun' : 'normal',
    title: 'Fun Linea',
    subtitle: 'Resident La-Linea Engine',
    loopDurationSec: Math.max(120, this.getNumberConfig('loopDurationSec', 210)),
    showTrackInfo: this.getBooleanConfig('showTrackInfo', true),
    showHelpText: this.getBooleanConfig('showHelpText', false),
    showSceneLabel: this.getBooleanConfig('showSceneLabel', false),
    simulateInputs: this.getBooleanConfig('simulateInputs', true),
    audioEnabled: false,
    audioRuntimeSupported: false,
    accentLevel: this.getNumberConfig('accentLevel', 1),
    residentRendererEnabled: this.isResidentRendererEnabled(),
    residentRendererServiceEnabled: this.isResidentRendererServiceEnabled(),
    storyPackId: this.getStringConfig('storyPackId', 'la_linea_audio_lock_01'),
    storyMode: this.getStringConfig('storyMode', 'auto'),
    lineThickness: this.getNumberConfig('lineThickness', 6),
    screen_width: this.getNumberConfig('screenWidth', 1920),
    screen_height: this.getNumberConfig('screenHeight', 550),
    fullscreen: this.getBooleanConfig('fullscreen', true),
    baselineYRatio: this.getNumberConfig('baselineYRatio', 0.905),
    actorScale: this.getNumberConfig('actorScale', 1.82),
    fullModeBackgroundPreset: this.getStringConfig('fullModeBackgroundPreset', 'dark_blue'),
    overlayBackgroundMode: this.getStringConfig('overlayBackgroundMode', 'transparent_hint'),
    lineColorPreset: this.getStringConfig('lineColorPreset', 'auto'),
    overlayTrackInfoStyle: this.getStringConfig('overlayTrackInfoStyle', 'minimal'),
    openedAt: Date.now()
  };
  this.writeJsonFile(this.settingsPath, payload);
};

ControllerFunLineaOverlay.prototype.pollState = function () {
  let state = null;
  try {
    state = this.commandRouter.volumioGetState();
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] volumioGetState failed: ' + err.message);
  }
  this.lastVolumioState = this.buildRendererState(state);
  this.writeStateIfChanged(this.lastVolumioState);
  return Promise.resolve(this.lastVolumioState);
};

ControllerFunLineaOverlay.prototype.startPolling = function () {
  this.stopPolling();
  this.pollState().catch(() => {});
  this.pollTimer = setInterval(() => {
    this.pollState().catch((err) => {
      this.logger.warn('[fun_linea_overlay] pollState failed: ' + err.message);
    });
  }, Math.max(300, this.getNumberConfig('pollStateIntervalMs', 750)));
};

ControllerFunLineaOverlay.prototype.stopPolling = function () {
  if (this.pollTimer) {
    clearInterval(this.pollTimer);
    this.pollTimer = null;
  }
};

ControllerFunLineaOverlay.prototype.isRendererEnabled = function () {
  return this.getBooleanConfig('enabled', true);
};

ControllerFunLineaOverlay.prototype.isResidentRendererEnabled = function () {
  return this.isRendererEnabled() && this.getBooleanConfig('residentRendererEnabled', true);
};

ControllerFunLineaOverlay.prototype.isResidentRendererServiceEnabled = function () {
  return this.isResidentRendererEnabled() && this.getBooleanConfig('residentRendererServiceEnabled', true);
};

ControllerFunLineaOverlay.prototype.getExternalRendererPid = function () {
  try {
    if (!fs.existsSync(this.rendererPidPath)) {
      return null;
    }
    const raw = String(fs.readFileSync(this.rendererPidPath, 'utf8') || '').trim();
    const pid = Number(raw);
    return Number.isInteger(pid) && pid > 1 ? pid : null;
  } catch (err) {
    this.logger.warn('[fun_linea_overlay] getExternalRendererPid failed: ' + err.message);
    return null;
  }
};

ControllerFunLineaOverlay.prototype.isPidAlive = function (pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (err) {
    return false;
  }
};

ControllerFunLineaOverlay.prototype.isRendererRunning = function () {
  if (this.rendererProcess) {
    return true;
  }
  const pid = this.getExternalRendererPid();
  return Boolean(pid && this.isPidAlive(pid));
};

ControllerFunLineaOverlay.prototype.shouldPreloadResidentRenderer = function () {
  return this.isResidentRendererEnabled() && !this.isResidentRendererServiceEnabled() && this.getBooleanConfig('preloadRendererOnPluginStart', true);
};

ControllerFunLineaOverlay.prototype.clearRendererRetryTimer = function () {
  if (this.rendererRetryTimer) {
    clearTimeout(this.rendererRetryTimer);
    this.rendererRetryTimer = null;
  }
};

ControllerFunLineaOverlay.prototype.scheduleResidentRendererStart = function (delayMs) {
  if (!this.shouldPreloadResidentRenderer()) {
    return;
  }
  this.clearRendererRetryTimer();
  this.rendererRetryTimer = setTimeout(() => {
    this.rendererRetryTimer = null;
    if (this.rendererProcess || !this.shouldPreloadResidentRenderer()) {
      return;
    }
    this.logger.info('[fun_linea_overlay] resident renderer preload attempt');
    this.startRenderer();
  }, Math.max(0, Number(delayMs) || 0));
};

ControllerFunLineaOverlay.prototype.startRenderer = function () {
  if (this.rendererProcess) {
    this.logger.info('[fun_linea_overlay] renderer already running (plugin child)');
    return;
  }
  if (this.isResidentRendererServiceEnabled() && this.isRendererRunning()) {
    this.logger.info('[fun_linea_overlay] resident renderer already running via service');
    return;
  }

  const residentMode = this.isResidentRendererEnabled();
  const useServiceLauncher = this.isResidentRendererServiceEnabled();
  const launcher = residentMode
    ? path.join(this.pluginDir, useServiceLauncher ? 'run_renderer_daemon.sh' : 'run_fun_linea.sh')
    : path.join(this.pluginDir, 'run_fun_linea.sh');
  this.clearRendererReadyFlag();
  this.rendererShutdownRequested = false;

  if (residentMode && !fs.existsSync('/tmp/.X11-unix/X0')) {
    this.logger.warn('[fun_linea_overlay] X11 socket /tmp/.X11-unix/X0 not found - resident preload may retry later');
  }

  this.logger.info('[fun_linea_overlay] starting renderer: ' + launcher + ' resident=' + JSON.stringify(residentMode));
  this.rendererOwnedByPlugin = true;
  this.rendererProcess = spawn('/bin/bash', [launcher], {
    cwd: this.pluginDir,
    env: Object.assign({}, process.env, {
      FUN_LINEA_PLUGIN_DIR: this.pluginDir,
      FUN_LINEA_RESIDENT: residentMode ? '1' : '0',
      DISPLAY: ':0',
      XAUTHORITY: '/home/volumio/.Xauthority',
      SDL_VIDEODRIVER: 'x11',
      SDL_AUDIODRIVER: 'dummy',
      FUN_LINEA_EXPECT_SERVICE_FLAG: useServiceLauncher ? '1' : '0',
      PYGAME_HIDE_SUPPORT_PROMPT: '1'
    }),
    detached: false,
    stdio: ['ignore', 'pipe', 'pipe']
  });

  this.rendererProcess.stdout.on('data', (data) => {
    this.logger.info('[fun_linea_overlay] ' + data.toString().trim());
  });

  this.rendererProcess.stderr.on('data', (data) => {
    this.logger.error('[fun_linea_overlay] ' + data.toString().trim());
  });

  this.rendererProcess.on('close', (code) => {
    this.logger.info('[fun_linea_overlay] renderer exited with code ' + code);
    this.rendererProcess = null;
    this.rendererOwnedByPlugin = false;
    if (!this.overlayVisible) {
      this.clearRendererReadyFlag();
    }
    if (!this.rendererShutdownRequested && this.shouldPreloadResidentRenderer()) {
      this.logger.warn('[fun_linea_overlay] resident renderer exited unexpectedly - scheduling retry');
      this.scheduleResidentRendererStart(this.getNumberConfig('residentRendererRetryMs', 5000));
    }
  });
};

ControllerFunLineaOverlay.prototype.stopRenderer = function () {
  this.rendererShutdownRequested = true;
  if (this.rendererProcess && this.rendererOwnedByPlugin) {
    try {
      this.rendererProcess.kill('SIGTERM');
    } catch (err) {
      this.logger.warn('[fun_linea_overlay] renderer SIGTERM failed: ' + err.message);
    }
    this.rendererProcess = null;
    this.rendererOwnedByPlugin = false;
  } else if (this.isResidentRendererServiceEnabled() && this.isRendererRunning()) {
    const pid = this.getExternalRendererPid();
    if (pid && this.isPidAlive(pid)) {
      try {
        process.kill(pid, 'SIGTERM');
        this.logger.info('[fun_linea_overlay] requested SIGTERM for service-managed renderer pid=' + pid);
      } catch (err) {
        this.logger.warn('[fun_linea_overlay] service-managed renderer SIGTERM failed: ' + err.message);
      }
    } else {
      this.logger.info('[fun_linea_overlay] stopRenderer skipped because resident renderer pid was not available');
    }
  }
  this.clearRendererReadyFlag();
};

ControllerFunLineaOverlay.prototype.emitSocketEvent = function (eventName, payload) {
  return new Promise((resolve, reject) => {
    const socket = io('http://127.0.0.1:3000', {
      forceNew: true,
      reconnection: false,
      transports: ['websocket', 'polling']
    });

    let done = false;
    const timer = setTimeout(() => finish(new Error('WebSocket timeout')), 4000);

    const finish = (err, result) => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      try { socket.disconnect(); } catch (disconnectErr) {}
      if (err) reject(err);
      else resolve(result || { success: true });
    };

    socket.on('connect', () => {
      socket.emit(eventName, payload || {});
      setTimeout(() => finish(null, { success: true }), 300);
    });
    socket.on('pushToastMessage', (msg) => {
      if (msg && msg.type === 'error') {
        finish(new Error(msg.message || 'Operation failed'));
      }
    });
    socket.on('connect_error', (err) => finish(err || new Error('connect_error')));
    socket.on('error', (err) => finish(err || new Error('socket_error')));
  });
};

ControllerFunLineaOverlay.prototype.navigateToBrowseRoot = function () {
  return this.emitSocketEvent('browseLibrary', { uri: '/' })
    .catch(() => this.emitSocketEvent('browseLibrary', { uri: '' }))
    .catch(() => ({ success: true }));
};

ControllerFunLineaOverlay.prototype.openFun = function () {
  this.logger.info('[fun_linea_overlay] openFun');
  if (!this.isRendererEnabled()) {
    return Promise.resolve({ success: false, reason: 'renderer-disabled' });
  }
  this.pauseScaleRendererIfRunning();
  this.setActiveOverlay('fun_linea');
  this.overlayVisible = true;
  this.writeSettingsFile();
  this.pollState().catch(() => {});
  if (!this.isRendererRunning()) {
    this.startRenderer();
  }
  return Promise.resolve({
    success: true,
    rendererRunning: this.isRendererRunning(),
    residentRendererEnabled: this.isResidentRendererEnabled()
  });
};

ControllerFunLineaOverlay.prototype.exitFunToBrowse = function (navigate) {
  this.logger.info('[fun_linea_overlay] exitFunToBrowse navigate=' + JSON.stringify(navigate));
  this.overlayVisible = false;
  this.releaseActiveOverlay('fun_linea');
  this.resumeScaleRendererIfPaused();
  this.writeSettingsFile();
  this.pollState().catch(() => {});
  if (this.isResidentRendererEnabled()) {
    this.clearRendererReadyFlag();
  } else {
    this.stopRenderer();
  }
  if (navigate === false) {
    return Promise.resolve({ success: true, rendererRunning: this.isRendererRunning() });
  }
  return Promise.resolve()
    .then(() => this.delay(150))
    .then(() => this.navigateToBrowseRoot())
    .then(() => ({ success: true, rendererRunning: this.isRendererRunning() }));
};

ControllerFunLineaOverlay.prototype.encoder1ShortPress = function () {
  return this.openFun();
};

ControllerFunLineaOverlay.prototype.encoder1LongPress = function () {
  return this.exitFunToBrowse(true);
};

ControllerFunLineaOverlay.prototype.gpio13OpenFun = function () {
  return this.openFun();
};

ControllerFunLineaOverlay.prototype.setFunMode = function () {
  return this.openFun();
};

ControllerFunLineaOverlay.prototype.setNormalMode = function () {
  return this.exitFunToBrowse(true);
};

ControllerFunLineaOverlay.prototype.getControlStatus = function () {
  return Promise.resolve({
    success: true,
    rendererRunning: this.isRendererRunning(),
    rendererReady: this.isRendererReady(),
    visible: this.overlayVisible,
    residentRendererEnabled: this.isResidentRendererEnabled(),
    residentRendererServiceEnabled: this.isResidentRendererServiceEnabled(),
    pluginName: PUBLIC_OVERLAY_NAME,
    sourceName: PUBLIC_SOURCE_LABEL,
    audioRuntimeSupported: false
  });
};

ControllerFunLineaOverlay.prototype.extractSettingValue = function (data, key, fallback) {
  if (!data || typeof data !== 'object') {
    return fallback;
  }
  if (Object.prototype.hasOwnProperty.call(data, key)) {
    return data[key];
  }
  const stack = [data];
  while (stack.length) {
    const item = stack.pop();
    if (!item || typeof item !== 'object') continue;
    if (Array.isArray(item)) {
      item.forEach((entry) => stack.push(entry));
      continue;
    }
    if (item.id === key && Object.prototype.hasOwnProperty.call(item, 'value')) {
      return item.value;
    }
    Object.keys(item).forEach((childKey) => {
      const child = item[childKey];
      if (child && typeof child === 'object') {
        stack.push(child);
      }
    });
  }
  return fallback;
};


ControllerFunLineaOverlay.prototype.readUIConfigFile = function () {
  const uiPath = path.join(this.pluginDir, 'UIConfig.json');
  return JSON.parse(fs.readFileSync(uiPath, 'utf8'));
};

ControllerFunLineaOverlay.prototype.getAvailableStoryPacks = function () {
  const storypacksDir = path.join(this.pluginDir, 'renderer', 'storypacks');
  const packs = [];
  try {
    fs.readdirSync(storypacksDir, { withFileTypes: true }).forEach((entry) => {
      if (!entry.isDirectory()) return;
      const manifestPath = path.join(storypacksDir, entry.name, 'manifest.json');
      let label = entry.name;
      try { label = JSON.parse(fs.readFileSync(manifestPath, 'utf8')).title || entry.name; } catch (err) {}
      packs.push({ id: entry.name, label });
    });
  } catch (err) {}
  return packs.length ? packs : [{ id: 'dog_line_visual_01', label: 'Dog Line Visual Pack 01' }];
};

ControllerFunLineaOverlay.prototype.getUIConfig = function () {
  const defer = libQ.defer();
  try {
    const uiconf = this.readUIConfigFile();
    const packs = this.getAvailableStoryPacks();
    const applyValue = (id, value) => {
      for (const section of (uiconf.sections || [])) {
        for (const item of (section.content || [])) {
          if (item.id === 'storyPackId') item.options = packs.map((pack) => ({ value: pack.id, label: pack.label }));
          if (item.id === id) item.value = value;
        }
      }
    };
    applyValue('storyPackId', this.getStringConfig('storyPackId', 'dog_line_visual_01'));
    applyValue('storyMode', this.getStringConfig('storyMode', 'auto'));
    applyValue('fullModeBackgroundPreset', this.getStringConfig('fullModeBackgroundPreset', 'dark_blue'));
    applyValue('overlayBackgroundMode', this.getStringConfig('overlayBackgroundMode', 'transparent_hint'));
    applyValue('lineColorPreset', this.getStringConfig('lineColorPreset', 'auto'));
    applyValue('baselineYRatio', this.getNumberConfig('baselineYRatio', 0.90));
    applyValue('actorScale', this.getNumberConfig('actorScale', 1.15));
    applyValue('lineThickness', this.getNumberConfig('lineThickness', 4));
    applyValue('showTrackInfo', this.getBooleanConfig('showTrackInfo', true));
    applyValue('showSceneLabel', this.getBooleanConfig('showSceneLabel', false));
    applyValue('targetVisibleFps', this.getNumberConfig('targetVisibleFps', 14));
    applyValue('pollStateIntervalMs', this.getNumberConfig('pollStateIntervalMs', 900));
    applyValue('residentRendererEnabled', this.getBooleanConfig('residentRendererEnabled', true));
    applyValue('residentRendererServiceEnabled', this.getBooleanConfig('residentRendererServiceEnabled', false));
    defer.resolve(uiconf);
  } catch (err) {
    this.logger.error('[fun_linea_overlay] getUIConfig failed: ' + err.stack);
    defer.reject(err);
  }
  return defer.promise;
};

ControllerFunLineaOverlay.prototype.setUIConfig = function (data) {
  const defer = libQ.defer();
  try {
    this.setConfigValue('storyPackId', String(this.extractSettingValue(data, 'storyPackId', this.getStringConfig('storyPackId', 'dog_line_visual_01'))));
    this.setConfigValue('storyMode', String(this.extractSettingValue(data, 'storyMode', this.getStringConfig('storyMode', 'auto'))));
    this.setConfigValue('fullModeBackgroundPreset', String(this.extractSettingValue(data, 'fullModeBackgroundPreset', this.getStringConfig('fullModeBackgroundPreset', 'dark_blue'))));
    this.setConfigValue('overlayBackgroundMode', String(this.extractSettingValue(data, 'overlayBackgroundMode', this.getStringConfig('overlayBackgroundMode', 'transparent_hint'))));
    this.setConfigValue('lineColorPreset', String(this.extractSettingValue(data, 'lineColorPreset', this.getStringConfig('lineColorPreset', 'auto'))));
    this.setConfigValue('baselineYRatio', Number(this.extractSettingValue(data, 'baselineYRatio', this.getNumberConfig('baselineYRatio', 0.90))));
    this.setConfigValue('actorScale', Number(this.extractSettingValue(data, 'actorScale', this.getNumberConfig('actorScale', 1.15))));
    this.setConfigValue('lineThickness', Number(this.extractSettingValue(data, 'lineThickness', this.getNumberConfig('lineThickness', 4))));
    this.setConfigValue('showTrackInfo', Boolean(this.extractSettingValue(data, 'showTrackInfo', this.getBooleanConfig('showTrackInfo', true))));
    this.setConfigValue('showSceneLabel', Boolean(this.extractSettingValue(data, 'showSceneLabel', this.getBooleanConfig('showSceneLabel', false))));
    this.setConfigValue('targetVisibleFps', Number(this.extractSettingValue(data, 'targetVisibleFps', this.getNumberConfig('targetVisibleFps', 14))));
    this.setConfigValue('pollStateIntervalMs', Number(this.extractSettingValue(data, 'pollStateIntervalMs', this.getNumberConfig('pollStateIntervalMs', 900))));
    this.setConfigValue('residentRendererEnabled', Boolean(this.extractSettingValue(data, 'residentRendererEnabled', this.getBooleanConfig('residentRendererEnabled', true))));
    this.setConfigValue('residentRendererServiceEnabled', Boolean(this.extractSettingValue(data, 'residentRendererServiceEnabled', this.getBooleanConfig('residentRendererServiceEnabled', false))));
    this.writeServiceEnableFlag();
    this.writeSettingsFile();
    this.pollState().catch(() => {});
    defer.resolve({ success: true, reloaded: true });
  } catch (err) {
    this.logger.error('[fun_linea_overlay] setUIConfig failed: ' + err.stack);
    defer.reject(err);
  }
  return defer.promise;
};

