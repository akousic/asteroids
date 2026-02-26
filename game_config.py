import json
import os
import pygame

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "user_settings.json")

DEFAULT_SETTINGS = {
    "audio": {
        "master": 0.8,
        "music": 0.6,
        "sfx": 0.9,
    },
    "controls": {
        "thrust": "w",
        "turn_left": "a",
        "turn_right": "d",
        "fire": "space",
        "pause": "p",
    },
}


class SettingsManager:
    def __init__(self) -> None:
        self.settings = self._load()

    def _load(self):
        os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
        if not os.path.exists(_CONFIG_PATH):
            return json.loads(json.dumps(DEFAULT_SETTINGS))
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = json.loads(json.dumps(DEFAULT_SETTINGS))
            merged["audio"].update(data.get("audio", {}))
            merged["controls"].update(data.get("controls", {}))
            return merged
        except Exception:
            return json.loads(json.dumps(DEFAULT_SETTINGS))

    def save(self):
        os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
        with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

    def reset_defaults(self):
        self.settings = json.loads(json.dumps(DEFAULT_SETTINGS))

    def key_bindings(self):
        out = {}
        for action, key_name in self.settings["controls"].items():
            try:
                out[action] = pygame.key.key_code(key_name)
            except Exception:
                out[action] = pygame.key.key_code(DEFAULT_SETTINGS["controls"][action])
        return out

    def set_binding(self, action: str, key_code: int):
        self.settings["controls"][action] = pygame.key.name(key_code)

    def has_conflict(self):
        values = list(self.settings["controls"].values())
        return len(values) != len(set(values))
