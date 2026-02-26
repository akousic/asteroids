"""
SoundManager — graceful audio system.

All sound loads are guarded with try/except so the game runs
silently if assets are missing (Epic 8 ships placeholder WAVs).

Heartbeat is driven by an alternating two-tone pattern that
speeds up as the asteroid count decreases.
"""
import os
import pygame

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")

# Map sound names to filenames
_SOUND_FILES = {
    "fire":              "fire.wav",
    "explosion_asteroid": "explosion_asteroid.wav",
    "explosion_ship":    "explosion_ship.wav",
    "explosion_saucer":  "explosion_saucer.wav",
    "saucer_large":      "saucer_large.wav",
    "saucer_small":      "saucer_small.wav",
    "extra_life":        "extra_life.wav",
    "hyperspace":        "hyperspace.wav",
    "heartbeat_hi":      "beat1.wav",
    "heartbeat_lo":      "beat2.wav",
}


class SoundManager:
    """Loads and plays game sounds. Silently degrades if files are missing."""

    def __init__(self) -> None:
        self._sounds: dict = {}
        self._heartbeat_timer = 0.0
        self._heartbeat_interval = 1.0   # seconds between beats (decreases with action)
        self._heartbeat_phase = 0        # alternates 0/1 for hi/lo beat
        self.master = 0.8
        self.music = 0.6
        self.sfx = 0.9

        if not pygame.mixer.get_init():
            return  # mixer not available

        for name, filename in _SOUND_FILES.items():
            path = os.path.join(_ASSETS_DIR, filename)
            try:
                self._sounds[name] = pygame.mixer.Sound(path)
            except (pygame.error, FileNotFoundError, OSError):
                pass  # missing sound — no crash

    def set_volumes(self, master: float, music: float, sfx: float) -> None:
        self.master = max(0.0, min(1.0, float(master)))
        self.music = max(0.0, min(1.0, float(music)))
        self.sfx = max(0.0, min(1.0, float(sfx)))

    def play(self, name: str) -> None:
        """Play a sound by name. No-op if sound is missing."""
        sound = self._sounds.get(name)
        if sound:
            try:
                # heartbeat treated as music-like layer, others as sfx
                layer = self.music if name.startswith("heartbeat") else self.sfx
                sound.set_volume(self.master * layer)
                sound.play()
            except pygame.error:
                pass

    def update_heartbeat(self, dt: float, asteroid_count: int) -> None:
        """Tick the heartbeat. Call every frame from _update_active."""
        # Interval shrinks as asteroid count decreases (more intense)
        target_interval = max(0.25, 1.0 - (10 - asteroid_count) * 0.07)
        # Smooth lerp toward target
        self._heartbeat_interval += (target_interval - self._heartbeat_interval) * dt * 2

        self._heartbeat_timer -= dt
        if self._heartbeat_timer <= 0:
            self._heartbeat_timer = self._heartbeat_interval
            beat_name = "heartbeat_hi" if self._heartbeat_phase == 0 else "heartbeat_lo"
            self.play(beat_name)
            self._heartbeat_phase = 1 - self._heartbeat_phase

    def stop_all(self) -> None:
        """Stop all currently playing sounds."""
        try:
            pygame.mixer.stop()
        except pygame.error:
            pass
