#!/usr/bin/env python3
import json
import math
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame

PLUGIN_DIR = Path(os.environ.get('FUN_LINEA_PLUGIN_DIR', '/data/plugins/user_interface/fun_linea_overlay'))
RUNTIME_DIR = PLUGIN_DIR / 'runtime'
STATE_PATH = RUNTIME_DIR / 'state.json'
SETTINGS_PATH = RUNTIME_DIR / 'settings.json'
READY_PATH = RUNTIME_DIR / 'renderer_ready.json'
PID_PATH = RUNTIME_DIR / 'renderer.pid'
STORYPACKS_DIR = PLUGIN_DIR / 'renderer' / 'storypacks'
ASSET_DIR = PLUGIN_DIR / 'renderer' / 'assets' / 'dog_line'
ACTIVE_OVERLAY_PATH = Path('/tmp/mediastreamer_active_overlay.json')

RUNNING = True

FULL_BG_PRESETS = {
    'dark_blue': (10, 22, 36),
    'dark_gray': (24, 24, 28),
    'dark_green': (12, 32, 20),
}
LINE_PRESETS = {
    'warm_white': (244, 242, 232),
    'cool_white': (232, 240, 248),
    'mint': (214, 246, 230),
    'amber': (255, 216, 160),
}


def handle_signal(signum, frame):
    global RUNNING
    RUNNING = False


def load_json(path: Path, default):
    try:
        if not path.exists():
            return default
        raw = path.read_text(encoding='utf-8').strip()
        if not raw:
            return default
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, type(default)) else default
    except Exception:
        return default


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def draw_text(surface, text: str, font, pos, color, align='left'):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if align == 'center':
        rect.center = (int(pos[0]), int(pos[1]))
    elif align == 'right':
        rect.topright = (int(pos[0]), int(pos[1]))
    else:
        rect.topleft = (int(pos[0]), int(pos[1]))
    surface.blit(img, rect)


class FunLineaRenderer:
    def __init__(self):
        self.settings: Dict[str, Any] = {
            'visible': False,
            'ui_mode': 'normal',
            'loopDurationSec': 180,
            'showTrackInfo': True,
            'showHelpText': False,
            'showSceneLabel': False,
            'pollStateIntervalMs': 900,
            'storyPackId': 'dog_line_visual_01',
            'storyMode': 'auto',
            'lineThickness': 4,
            'targetVisibleFps': 14,
            'hiddenSleepMs': 350,
            'hiddenReloadMs': 1200,
            'screen_width': 1920,
            'screen_height': 550,
            'fullscreen': True,
            'baselineYRatio': 0.90,
            'actorScale': 1.15,
            'fullModeBackgroundPreset': 'dark_blue',
            'overlayBackgroundMode': 'transparent_hint',
            'lineColorPreset': 'auto'
        }
        self.state: Dict[str, Any] = {
            'status': 'stop',
            'title': 'Fun Linea',
            'artist': 'Dog Line',
            'service': '',
            'ui_mode': 'normal'
        }
        self.settings_mtime = None
        self.state_mtime = None
        self.resident_mode = str(os.environ.get('FUN_LINEA_RESIDENT', '0')).strip().lower() in ('1', 'true', 'yes', 'on')
        self.window_visible = False
        self.screen = None
        self.clock = None
        self.size = (0, 0)
        self.fonts = {}
        self.first_frame_presented = False
        self.last_runtime_reload_at = 0.0
        self.last_active_overlay_check_at = 0.0
        self.last_known_active_overlay = 'none'
        self.storypack: Dict[str, Any] = {}
        self.scene_pool: List[Dict[str, Any]] = []
        self.sequence: List[Dict[str, Any]] = []
        self.current_sequence_seed = None
        self.sequence_loop_counter = 0
        self.loaded_storypack_id = None
        self.assets: Dict[str, pygame.Surface] = {}
        self.tint_cache: Dict[Tuple[str, int, int, Tuple[int, int, int], int], pygame.Surface] = {}

    def load_runtime_json(self, path: Path, current: Dict[str, Any], attr_name: str):
        try:
            mtime = path.stat().st_mtime
        except FileNotFoundError:
            return
        prev = getattr(self, attr_name)
        if prev != mtime:
            current.update(load_json(path, {}))
            setattr(self, attr_name, mtime)

    def reload_runtime(self, force=False):
        now = time.monotonic()
        interval = self.hidden_reload_seconds() if not self.window_visible else max(0.2, float(self.settings.get('pollStateIntervalMs', 900)) / 1000.0)
        if force:
            self.settings_mtime = None
            self.state_mtime = None
            self.last_runtime_reload_at = 0.0
        if not force and (now - self.last_runtime_reload_at) < interval:
            return
        self.last_runtime_reload_at = now
        self.load_runtime_json(SETTINGS_PATH, self.settings, 'settings_mtime')
        self.load_runtime_json(STATE_PATH, self.state, 'state_mtime')

    def write_ready_marker(self, stage='ready'):
        try:
            READY_PATH.write_text(json.dumps({'ready': True, 'stage': stage, 'ts': time.time(), 'size': list(self.size)}), encoding='utf-8')
        except Exception:
            pass

    def clear_ready_marker(self):
        try:
            if READY_PATH.exists():
                READY_PATH.unlink()
        except Exception:
            pass

    def write_pid_marker(self):
        try:
            PID_PATH.write_text(str(os.getpid()), encoding='utf-8')
        except Exception:
            pass

    def clear_pid_marker(self):
        try:
            if PID_PATH.exists():
                PID_PATH.unlink()
        except Exception:
            pass

    def init_fonts(self):
        h = self.size[1]
        self.fonts = {
            'title': pygame.font.SysFont('DejaVu Sans', max(18, int(h * 0.052))),
            'body': pygame.font.SysFont('DejaVu Sans', max(13, int(h * 0.030))),
            'small': pygame.font.SysFont('DejaVu Sans', max(11, int(h * 0.024))),
        }

    def build_display_flags(self, visible: bool) -> int:
        flags = pygame.NOFRAME
        if visible and bool(self.settings.get('fullscreen', True)):
            flags |= pygame.FULLSCREEN
        if not visible:
            flags |= getattr(pygame, 'HIDDEN', 0)
        return flags

    def init_display(self, force=False, visible: Optional[bool] = None):
        width = int(self.settings.get('screen_width', self.settings.get('screenWidth', 1920)))
        height = int(self.settings.get('screen_height', self.settings.get('screenHeight', 550)))
        target = (width, height)
        requested_visible = self.window_visible if visible is None else bool(visible)
        if (not force and self.screen is not None and target == self.size and requested_visible == self.window_visible):
            return
        self.screen = pygame.display.set_mode(target, self.build_display_flags(requested_visible))
        pygame.display.set_caption('Fun Linea Overlay')
        self.size = target
        self.window_visible = requested_visible
        self.clock = self.clock or pygame.time.Clock()
        self.init_fonts()
        self.clear_ready_marker()

    def sync_window_visibility(self):
        desired_visible = True
        if self.resident_mode:
            desired_visible = bool(self.settings.get('visible', False)) or str(self.state.get('ui_mode') or self.settings.get('ui_mode') or 'normal').lower() == 'fun'
        if self.screen is None:
            self.init_display(force=True, visible=desired_visible)
            return
        if desired_visible == self.window_visible:
            return
        self.window_visible = desired_visible
        self.clear_ready_marker()
        self.screen = pygame.display.set_mode(self.size, self.build_display_flags(desired_visible))
        pygame.display.set_caption('Fun Linea Overlay')

    def active_overlay_owner(self) -> str:
        now = time.monotonic()
        if now - self.last_active_overlay_check_at < 0.5:
            return self.last_known_active_overlay
        owner = 'none'
        try:
            raw = ACTIVE_OVERLAY_PATH.read_text(encoding='utf-8').strip()
            if raw:
                parsed = json.loads(raw)
                owner = str(parsed.get('owner') or 'none').strip().lower()
        except Exception:
            owner = 'none'
        self.last_active_overlay_check_at = now
        self.last_known_active_overlay = owner
        return owner

    def is_foreground_owner(self) -> bool:
        owner = self.active_overlay_owner()
        return owner in ('none', 'fun_linea')

    def visible_fps(self) -> int:
        return max(8, min(20, int(self.settings.get('targetVisibleFps', 14))))

    def hidden_sleep_seconds(self) -> float:
        return max(0.08, min(2.0, float(self.settings.get('hiddenSleepMs', 350)) / 1000.0))

    def hidden_reload_seconds(self) -> float:
        return max(0.5, min(5.0, float(self.settings.get('hiddenReloadMs', 1200)) / 1000.0))

    def load_storypack(self):
        requested_id = str(self.settings.get('storyPackId') or 'dog_line_visual_01').strip()
        pack_dir = STORYPACKS_DIR / requested_id
        if not pack_dir.exists():
            requested_id = 'dog_line_visual_01'
            pack_dir = STORYPACKS_DIR / requested_id
        self.loaded_storypack_id = requested_id
        self.storypack = load_json(pack_dir / 'manifest.json', {})
        self.scene_pool = [s for s in load_json(pack_dir / 'stories' / 'generated' / 'scenes.json', []) if isinstance(s, dict) and s.get('kind')]
        if not self.scene_pool:
            self.scene_pool = self.default_scenes()

    def default_scenes(self) -> List[Dict[str, Any]]:
        return [
            {'scene_id': 'dog_idle_overlay', 'title_de': 'Dog Line — Idle', 'duration_sec': 14, 'kind': 'dog_idle'},
            {'scene_id': 'dog_sniff_marker', 'title_de': 'Dog Line — Schnüffeln', 'duration_sec': 16, 'kind': 'dog_sniff_marker'},
            {'scene_id': 'dog_head_tilt', 'title_de': 'Dog Line — Kopf schief', 'duration_sec': 14, 'kind': 'dog_head_tilt'},
            {'scene_id': 'dog_gap_hop', 'title_de': 'Dog Line — Linienlücke', 'duration_sec': 12, 'kind': 'dog_gap_hop'},
            {'scene_id': 'dog_note_chase', 'title_de': 'Dog Line — Notenjagd', 'duration_sec': 16, 'kind': 'dog_note_chase'},
            {'scene_id': 'dog_sit_watch', 'title_de': 'Dog Line — Lauschen', 'duration_sec': 16, 'kind': 'dog_sit_watch'},
        ]

    def choose_sequence(self, total_duration: float):
        if not self.scene_pool:
            self.sequence = []
            return
        mode = str(self.settings.get('storyMode') or 'auto').strip().lower()
        if mode == 'sequential':
            self.sequence = list(self.scene_pool)
            return
        seed = self.sequence_loop_counter
        if self.current_sequence_seed == seed and self.sequence:
            return
        ordered = list(self.scene_pool)
        if ordered:
            shift = seed % len(ordered)
            ordered = ordered[shift:] + ordered[:shift]
        seq = []
        acc = 0.0
        for scene in ordered:
            seq.append(scene)
            acc += float(scene.get('duration_sec', 14))
            if acc >= total_duration:
                break
        self.sequence = seq or ordered[:3]
        self.current_sequence_seed = seed

    def current_scene(self, elapsed: float, total_duration: float):
        self.choose_sequence(total_duration)
        if not self.sequence:
            return None, 0.0
        t = elapsed
        for scene in self.sequence:
            dur = float(scene.get('duration_sec', 14))
            if t < dur:
                return scene, t / max(0.001, dur)
            t -= dur
        return self.sequence[-1], 0.999

    def get_palette(self, playback_overlay: bool):
        bg_key = str(self.settings.get('fullModeBackgroundPreset') or 'dark_blue')
        bg = FULL_BG_PRESETS.get(bg_key, FULL_BG_PRESETS['dark_blue'])
        if playback_overlay and str(self.settings.get('overlayBackgroundMode') or 'transparent_hint') == 'transparent_hint':
            bg = tuple(int(c * 0.38) for c in bg)
        line_key = str(self.settings.get('lineColorPreset') or 'auto')
        if line_key == 'auto':
            line = LINE_PRESETS['amber'] if playback_overlay else LINE_PRESETS['warm_white']
        else:
            line = LINE_PRESETS.get(line_key, LINE_PRESETS['warm_white'])
        soft = tuple(max(0, min(255, int(c * 0.70))) for c in line)
        accent = LINE_PRESETS['mint'] if playback_overlay else LINE_PRESETS['cool_white']
        return bg, line, soft, accent

    def line_width(self) -> int:
        return max(2, int(self.settings.get('lineThickness', 4)))

    def baseline_y(self) -> float:
        return self.size[1] * clamp(float(self.settings.get('baselineYRatio', 0.90)), 0.72, 0.94)

    def actor_scale(self) -> float:
        return clamp(float(self.settings.get('actorScale', 1.15)), 0.7, 2.4)

    def load_assets(self):
        for name in ('idle', 'sniff', 'head_tilt', 'hop', 'sit'):
            p = ASSET_DIR / f'{name}.png'
            if p.exists():
                self.assets[name] = pygame.image.load(str(p)).convert_alpha()

    def get_pose_surface(self, name: str, width: int, height: int, color: Tuple[int, int, int], facing: int = 1):
        width = max(24, int(width))
        height = max(24, int(height))
        key = (name, width, height, color, 1 if facing >= 0 else -1)
        if key in self.tint_cache:
            return self.tint_cache[key]
        base = self.assets.get(name) or self.assets.get('idle')
        if base is None:
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            self.tint_cache[key] = surf
            return surf
        surf = pygame.transform.smoothscale(base, (width, height))
        if facing < 0:
            surf = pygame.transform.flip(surf, True, False)
        tint = surf.copy()
        tint.fill((color[0], color[1], color[2], 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.tint_cache[key] = tint
        return tint

    def draw_baseline(self, line_color, gap: Optional[Tuple[float, float]] = None):
        y = int(self.baseline_y())
        lw = self.line_width()
        if not gap:
            pygame.draw.line(self.screen, line_color, (0, y), (self.size[0], y), lw)
            return y
        left, right = int(gap[0]), int(gap[1])
        pygame.draw.line(self.screen, line_color, (0, y), (max(0, left), y), lw)
        pygame.draw.line(self.screen, line_color, (min(self.size[0], right), y), (self.size[0], y), lw)
        return y

    def draw_note(self, x: float, y: float, line_color, swing: float = 0.0):
        lw = self.line_width()
        x = int(x)
        y = int(y + swing)
        pygame.draw.line(self.screen, line_color, (x, y), (x, y - 22), lw)
        pygame.draw.line(self.screen, line_color, (x, y - 22), (x + 18, y - 32), lw)
        pygame.draw.circle(self.screen, line_color, (x - 4, y), 8, lw)
        pygame.draw.circle(self.screen, line_color, (x + 14, y - 10), 8, lw)

    def blit_actor(self, pose: str, center_x: float, ground_y: float, scale: float, color, facing: int = 1, offset_y: float = 0.0):
        dims = {
            'idle': (220, 200),
            'sniff': (340, 220),
            'head_tilt': (220, 200),
            'hop': (280, 220),
            'sit': (190, 180),
        }
        bw, bh = dims.get(pose, dims['idle'])
        bw = int(bw * scale)
        bh = int(bh * scale)
        surf = self.get_pose_surface(pose, bw, bh, color, facing)
        rect = surf.get_rect()
        rect.midbottom = (int(center_x), int(ground_y + offset_y))
        self.screen.blit(surf, rect)
        return rect

    def render_scene(self, scene: Dict[str, Any], t: float, playback_overlay: bool, line_color, soft, accent):
        kind = str(scene.get('kind') or 'dog_idle')
        w, _ = self.size
        full_stage = not playback_overlay
        base_scale = self.actor_scale() * (1.35 if full_stage else 0.82)
        base_y = self.draw_baseline(line_color)
        anchor_x = w * (0.56 if full_stage else 0.82)
        if kind == 'dog_idle':
            bob = math.sin(t * math.pi * 2.0) * (2.0 if full_stage else 1.0)
            self.blit_actor('idle', anchor_x, base_y, base_scale, line_color, 1, offset_y=bob)
        elif kind == 'dog_sniff_marker':
            marker_x = w * (0.70 if full_stage else 0.86)
            pygame.draw.circle(self.screen, accent, (int(marker_x), int(base_y - 2)), max(4, self.line_width() + 1), 1)
            nose_push = math.sin(t * math.pi * 2.0) * 6.0
            self.blit_actor('sniff', marker_x - (180 * base_scale) + nose_push, base_y, base_scale * 1.02, line_color, 1, 0)
        elif kind == 'dog_head_tilt':
            sway = math.sin(t * math.pi * 2.0) * 8.0
            facing = 1 if t < 0.5 else -1
            self.blit_actor('head_tilt', anchor_x + sway, base_y, base_scale, line_color, facing, 0)
        elif kind == 'dog_gap_hop':
            gap_center = w * (0.62 if full_stage else 0.80)
            gap_w = 120 if full_stage else 70
            self.draw_baseline(line_color, gap=(gap_center - gap_w / 2, gap_center + gap_w / 2))
            x0 = gap_center - gap_w * 0.9
            x1 = gap_center + gap_w * 0.9
            x = x0 + (x1 - x0) * t
            arc = math.sin(t * math.pi) * (70 if full_stage else 42)
            self.blit_actor('hop', x, base_y, base_scale, line_color, 1, -arc)
        elif kind == 'dog_note_chase':
            note_x = w * (0.70 if full_stage else 0.88)
            note_y = base_y - (74 if full_stage else 58)
            self.draw_note(note_x, note_y, accent, swing=math.sin(t * math.pi * 4.0) * 6.0)
            x = note_x - (170 * base_scale) + math.sin(t * math.pi * 2.0) * 24.0
            pose = 'sniff' if t < 0.5 else 'hop'
            self.blit_actor(pose, x, base_y, base_scale, line_color, 1, -(10 if pose == 'hop' else 0))
        elif kind == 'dog_sit_watch':
            x = w * (0.64 if full_stage else 0.84)
            self.blit_actor('sit', x, base_y, base_scale * 0.95, line_color, 1, 0)
            self.draw_note(x + (140 * base_scale), base_y - 62, accent, swing=math.sin(t * math.pi * 2.0) * 4.0)
        else:
            self.blit_actor('idle', anchor_x, base_y, base_scale, line_color, 1, 0)

    def draw_frame(self, elapsed: float):
        total_duration = max(60.0, float(self.settings.get('loopDurationSec', 180)))
        scene, local_t = self.current_scene(elapsed, total_duration)
        playback_overlay = str(self.state.get('status') or 'stop').lower() == 'play' and str(self.settings.get('overlayBackgroundMode') or 'transparent_hint') == 'transparent_hint'
        bg, line_color, soft, accent = self.get_palette(playback_overlay)
        self.screen.fill(bg)
        if scene is None:
            self.draw_baseline(line_color)
            return
        self.render_scene(scene, local_t, playback_overlay, line_color, soft, accent)
        if bool(self.settings.get('showSceneLabel', False)):
            draw_text(self.screen, str(scene.get('title_de') or scene.get('scene_id') or 'Dog Line')[:80], self.fonts['small'], (26, 16), soft)
        if bool(self.settings.get('showTrackInfo', True)):
            title = str(self.state.get('title') or '').strip() or 'Fun Linea'
            artist = str(self.state.get('artist') or '').strip()
            meta = title if not artist else f'{title} — {artist}'
            draw_text(self.screen, meta[:96], self.fonts['body'], (self.size[0] - 24, self.size[1] - 52), line_color, align='right')
            service = str(self.state.get('service') or '').strip()
            status = str(self.state.get('status') or 'stop').strip()
            sub = ('Volumio: ' + status) if not service else ('Volumio: ' + status + ' / ' + service)
            draw_text(self.screen, sub[:96], self.fonts['small'], (self.size[0] - 24, self.size[1] - 28), soft, align='right')

    def run(self):
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        self.write_pid_marker()
        pygame.display.init()
        pygame.font.init()
        self.reload_runtime(force=True)
        self.load_storypack()
        self.load_assets()
        initial_visible = True if not self.resident_mode else bool(self.settings.get('visible', False))
        self.init_display(force=True, visible=initial_visible)
        loop_duration = max(60.0, float(self.settings.get('loopDurationSec', 180)))
        self.choose_sequence(loop_duration)
        loop_start = time.monotonic()
        global RUNNING
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                    RUNNING = False
            self.reload_runtime()
            self.sync_window_visibility()
            if str(self.settings.get('storyPackId') or '').strip() != str(self.loaded_storypack_id or ''):
                self.load_storypack()
                self.current_sequence_seed = None
            if self.window_visible and self.is_foreground_owner():
                elapsed = (time.monotonic() - loop_start) % loop_duration
                if elapsed < 0.04 and self.first_frame_presented:
                    self.sequence_loop_counter += 1
                    self.current_sequence_seed = None
                    self.choose_sequence(loop_duration)
                self.draw_frame(elapsed)
                pygame.display.flip()
                if not self.first_frame_presented:
                    self.first_frame_presented = True
                    self.write_ready_marker('first-visible-frame')
                self.clock.tick(self.visible_fps())
            else:
                if self.window_visible and not self.is_foreground_owner():
                    self.window_visible = False
                    self.clear_ready_marker()
                    self.screen = pygame.display.set_mode(self.size, self.build_display_flags(False))
                    pygame.display.set_caption('Fun Linea Overlay')
                time.sleep(self.hidden_sleep_seconds())
        self.clear_ready_marker()
        self.clear_pid_marker()
        pygame.display.quit()
        pygame.font.quit()
        return 0


def main():
    renderer = FunLineaRenderer()
    return renderer.run()


if __name__ == '__main__':
    sys.exit(main())
