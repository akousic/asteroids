import pygame
from typing import Optional

AUDIO_FIELDS = ["master", "music", "sfx"]
CONTROL_FIELDS = ["thrust", "turn_left", "turn_right", "fire", "pause"]


class SettingsOverlay:
    def __init__(self, settings_mgr):
        self.settings_mgr = settings_mgr
        self.tab = 0  # 0 audio, 1 controls
        self.index = 0
        self.message = ""
        self.rebinding: Optional[str] = None

        # staged copy
        self.audio = dict(settings_mgr.settings["audio"])
        self.controls = dict(settings_mgr.settings["controls"])

    def _items(self):
        if self.tab == 0:
            return AUDIO_FIELDS + ["save", "cancel", "reset"]
        return CONTROL_FIELDS + ["save", "cancel", "reset"]

    def _validate_controls(self):
        vals = list(self.controls.values())
        return len(vals) == len(set(vals))

    def _apply_to_manager(self):
        self.settings_mgr.settings["audio"] = dict(self.audio)
        self.settings_mgr.settings["controls"] = dict(self.controls)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if self.rebinding:
            key_name = pygame.key.name(event.key)
            self.controls[self.rebinding] = key_name
            self.rebinding = None
            if not self._validate_controls():
                self.message = "Conflict: duplicate key assignment"
            else:
                self.message = f"Bound successfully"
            return None

        items = self._items()

        if event.key in (pygame.K_TAB,):
            self.tab = 1 - self.tab
            self.index = 0
            self.message = ""
            return None
        if event.key in (pygame.K_UP, pygame.K_w):
            self.index = (self.index - 1) % len(items)
            return None
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.index = (self.index + 1) % len(items)
            return None

        active = items[self.index]

        if self.tab == 0 and active in AUDIO_FIELDS:
            step = 0.05
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.audio[active] = max(0.0, round(self.audio[active] - step, 2))
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.audio[active] = min(1.0, round(self.audio[active] + step, 2))
            return None

        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if active in CONTROL_FIELDS:
                self.rebinding = active
                self.message = f"Press new key for {active}..."
                return None
            if active == "save":
                if not self._validate_controls():
                    self.message = "Cannot save: duplicate keybinds"
                    return None
                self._apply_to_manager()
                self.settings_mgr.save()
                self.message = "Settings saved"
                return "save"
            if active == "cancel":
                return "cancel"
            if active == "reset":
                self.audio = dict(self.settings_mgr.settings["audio"])
                self.controls = dict(self.settings_mgr.settings["controls"])
                # reset defaults explicitly
                from game_config import DEFAULT_SETTINGS
                self.audio = dict(DEFAULT_SETTINGS["audio"])
                self.controls = dict(DEFAULT_SETTINGS["controls"])
                self.message = "Defaults restored (save to apply)"
                return None

        if event.key in (pygame.K_ESCAPE,):
            return "cancel"

        return None

    def draw(self, screen):
        w, h = screen.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(w * 0.18, h * 0.12, w * 0.64, h * 0.76)
        pygame.draw.rect(screen, (20, 28, 44), panel, border_radius=14)
        pygame.draw.rect(screen, (120, 140, 180), panel, width=2, border_radius=14)

        title_font = pygame.font.SysFont(None, 46)
        text_font = pygame.font.SysFont(None, 30)
        small_font = pygame.font.SysFont(None, 24)

        title = title_font.render("SETTINGS", True, (240, 245, 255))
        screen.blit(title, (panel.x + 24, panel.y + 18))

        tabs = ["Audio", "Controls"]
        tx = panel.x + 24
        for i, t in enumerate(tabs):
            active = i == self.tab
            r = pygame.Rect(tx, panel.y + 70, 120, 34)
            pygame.draw.rect(screen, (70, 96, 160) if active else (40, 54, 82), r, border_radius=8)
            label = text_font.render(t, True, (255, 255, 255))
            screen.blit(label, (r.x + 20, r.y + 6))
            tx += 132

        y = panel.y + 130
        items = self._items()
        for idx, key in enumerate(items):
            selected = idx == self.index
            color = (255, 230, 150) if selected else (230, 235, 245)

            if self.tab == 0 and key in AUDIO_FIELDS:
                v = self.audio[key]
                text = f"{key.title():<12} {int(v*100):>3}%   (←/→)"
            elif self.tab == 1 and key in CONTROL_FIELDS:
                text = f"{key.replace('_', ' ').title():<12} {self.controls[key]:>10}   (Enter to rebind)"
            else:
                text = key.upper()

            surf = text_font.render(text, True, color)
            screen.blit(surf, (panel.x + 28, y))
            y += 40

        helper = "TAB switch section | ↑/↓ select | ENTER confirm | ESC back"
        hs = small_font.render(helper, True, (180, 190, 210))
        screen.blit(hs, (panel.x + 24, panel.bottom - 48))

        if self.rebinding:
            msg = small_font.render(f"Listening: press key for {self.rebinding}", True, (255, 220, 120))
            screen.blit(msg, (panel.x + 24, panel.bottom - 78))
        elif self.message:
            msg = small_font.render(self.message, True, (140, 230, 170))
            screen.blit(msg, (panel.x + 24, panel.bottom - 78))
