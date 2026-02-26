"""
Integration tests for the Asteroids game.

Tests run without a display window using pygame.display.set_mode() with
the NOFRAME | HIDDEN flags or by mocking the display surface.

Coverage targets the core game systems:
- Module imports
- Game object lifecycle (ship, bullet, asteroid, saucer, particle)
- Collision detection
- Score / lives / wave logic
- High score persistence
- State machine transitions
"""
import sys
import os
import json
import math
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import pytest

# Initialize pygame without display for headless testing
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
pygame.init()
pygame.display.set_mode((1280, 720), pygame.NOFRAME)


# ── Module import smoke tests ─────────────────────────────────
class TestModuleImports:
    def test_import_utils(self):
        import utils
        assert hasattr(utils, "wrap_position")
        assert hasattr(utils, "circles_collide")
        assert hasattr(utils, "rotate_points")

    def test_import_settings(self):
        import settings
        assert settings.SCREEN_WIDTH == 1280
        assert settings.SCREEN_HEIGHT == 720
        assert settings.FPS == 60

    def test_import_ship(self):
        from ship import PlayerShip
        assert PlayerShip is not None

    def test_import_bullet(self):
        from bullet import Bullet
        assert Bullet is not None

    def test_import_asteroid(self):
        from asteroid import Asteroid
        assert Asteroid is not None

    def test_import_saucer(self):
        from saucer import Saucer
        assert Saucer is not None

    def test_import_particle(self):
        from particle import ExplosionParticle
        assert ExplosionParticle is not None

    def test_import_hud(self):
        from hud import HUD
        assert HUD is not None

    def test_import_menu(self):
        from menu import TitleScreen, GameOverScreen
        assert TitleScreen is not None
        assert GameOverScreen is not None

    def test_import_highscore(self):
        from highscore import load_high_score, save_high_score
        assert callable(load_high_score)
        assert callable(save_high_score)

    def test_import_sounds(self):
        from sounds import SoundManager
        assert SoundManager is not None


# ── PlayerShip tests ──────────────────────────────────────────
class TestPlayerShip:
    def setup_method(self):
        from ship import PlayerShip
        self.ship = PlayerShip(640, 360)

    def test_initial_position(self):
        assert self.ship.pos.x == pytest.approx(640)
        assert self.ship.pos.y == pytest.approx(360)

    def test_initial_velocity_zero(self):
        assert self.ship.vel.length() == pytest.approx(0)

    def test_initial_alive(self):
        assert self.ship.alive is True

    def test_update_applies_drag(self):
        self.ship.vel = pygame.Vector2(100, 0)
        self.ship.update(1 / 60)
        # After one frame with drag, speed should be slightly less than 100
        assert self.ship.vel.length() < 100

    def test_speed_cap(self):
        from settings import MAX_SPEED
        self.ship.vel = pygame.Vector2(MAX_SPEED * 2, 0)
        self.ship.update(1 / 60)
        assert self.ship.vel.length() <= MAX_SPEED + 0.01

    def test_wrap_right_edge(self):
        from settings import SCREEN_WIDTH
        self.ship.pos = pygame.Vector2(SCREEN_WIDTH + 10, 360)
        self.ship.vel = pygame.Vector2(0, 0)
        self.ship.update(1 / 60)
        assert self.ship.pos.x < SCREEN_WIDTH

    def test_respawn_resets_state(self):
        self.ship.alive = False
        self.ship.vel = pygame.Vector2(100, 100)
        self.ship.respawn(640, 360)
        assert self.ship.alive is True
        assert self.ship.vel.length() == pytest.approx(0)
        assert self.ship.invincible is True

    def test_has_radius(self):
        assert hasattr(self.ship, "RADIUS")
        assert self.ship.RADIUS > 0

    def test_invincibility_expires(self):
        self.ship.invincible = True
        self.ship.invincibility_timer = 0.1
        self.ship.update(0.2)
        assert self.ship.invincible is False


# ── Bullet tests ──────────────────────────────────────────────
class TestBullet:
    def setup_method(self):
        from bullet import Bullet
        self.Bullet = Bullet

    def test_player_bullet_moves(self):
        b = self.Bullet(pygame.Vector2(640, 360), 0, pygame.Vector2(0, 0))
        x0 = b.pos.x
        b.update(0.1)
        # bullet moving upward (angle=0 → nose up → -Y direction)
        assert b.pos.y < 360

    def test_bullet_expires(self):
        from settings import BULLET_LIFETIME
        b = self.Bullet(pygame.Vector2(640, 360), 0, pygame.Vector2(0, 0))
        b.update(BULLET_LIFETIME + 0.1)
        assert b.expired is True

    def test_player_bullet_flag(self):
        b = self.Bullet(pygame.Vector2(0, 0), 0, pygame.Vector2(0, 0), is_player_bullet=True)
        assert b.is_player_bullet is True

    def test_saucer_bullet_flag(self):
        b = self.Bullet(pygame.Vector2(0, 0), 0, pygame.Vector2(0, 0), is_player_bullet=False)
        assert b.is_player_bullet is False

    def test_wraps_screen(self):
        from settings import SCREEN_HEIGHT
        b = self.Bullet(pygame.Vector2(640, -5), 180, pygame.Vector2(0, 0))
        b.update(0.01)
        assert 0 <= b.pos.y <= SCREEN_HEIGHT


# ── Asteroid tests ────────────────────────────────────────────
class TestAsteroid:
    def setup_method(self):
        from asteroid import Asteroid
        self.Asteroid = Asteroid

    def test_spawn_large_creates_asteroid(self):
        ship_pos = pygame.Vector2(640, 360)
        a = self.Asteroid.spawn_large(ship_pos)
        assert a.size == "large"

    def test_large_has_correct_radius(self):
        from settings import ASTEROID_LARGE_RADIUS
        a = self.Asteroid.spawn_large(pygame.Vector2(640, 360))
        assert a.radius == ASTEROID_LARGE_RADIUS

    def test_split_large_yields_two_mediums(self):
        a = self.Asteroid.spawn_large(pygame.Vector2(640, 360))
        children = a.split()
        assert len(children) == 2
        assert all(c.size == "medium" for c in children)

    def test_split_medium_yields_two_smalls(self):
        a = self.Asteroid(pygame.Vector2(0, 0), pygame.Vector2(0, 0), "medium")
        children = a.split()
        assert len(children) == 2
        assert all(c.size == "small" for c in children)

    def test_split_small_yields_no_children(self):
        a = self.Asteroid(pygame.Vector2(0, 0), pygame.Vector2(0, 0), "small")
        children = a.split()
        assert len(children) == 0

    def test_asteroid_moves(self):
        a = self.Asteroid(pygame.Vector2(100, 100), pygame.Vector2(50, 0), "large")
        a.update(1.0)
        assert a.pos.x != pytest.approx(100)

    def test_asteroid_wraps(self):
        from settings import SCREEN_WIDTH
        a = self.Asteroid(pygame.Vector2(SCREEN_WIDTH + 10, 100), pygame.Vector2(0, 0), "large")
        a.update(0.01)
        assert a.pos.x < SCREEN_WIDTH


# ── Saucer tests ──────────────────────────────────────────────
class TestSaucer:
    def setup_method(self):
        from saucer import Saucer
        self.Saucer = Saucer

    def test_large_saucer_has_large_radius(self):
        from settings import SAUCER_LARGE_RADIUS
        s = self.Saucer(large=True)
        assert s.radius == SAUCER_LARGE_RADIUS

    def test_small_saucer_has_small_radius(self):
        from settings import SAUCER_SMALL_RADIUS
        s = self.Saucer(large=False)
        assert s.radius == SAUCER_SMALL_RADIUS

    def test_saucer_moves(self):
        s = self.Saucer(large=True)
        x0 = s.pos.x
        s.update(0.5, None)
        # Should have moved
        assert s.pos.x != pytest.approx(x0)

    def test_saucer_fires_after_interval(self):
        from settings import SAUCER_LARGE_FIRE_INTERVAL
        s = self.Saucer(large=True)
        s._fire_timer = 0.01
        s.update(0.05, None)
        assert s.wants_to_fire() is True

    def test_saucer_create_bullet(self):
        from bullet import Bullet
        s = self.Saucer(large=True)
        b = s.create_bullet(Bullet, None)
        assert b is not None


# ── Particle tests ────────────────────────────────────────────
class TestParticle:
    def test_particle_expires(self):
        from particle import ExplosionParticle
        p = ExplosionParticle(pygame.Vector2(640, 360))
        # Override lifetime for fast expiry
        p._lifetime = 0.01
        p._max_lifetime = 0.01
        p.update(0.1)
        assert p.expired is True

    def test_particle_moves(self):
        from particle import ExplosionParticle
        p = ExplosionParticle(pygame.Vector2(640, 360))
        x0, y0 = p.pos.x, p.pos.y
        p.update(0.1)
        # Particle should have moved (unless velocity is zero, very unlikely)
        moved = (p.pos.x != pytest.approx(x0) or p.pos.y != pytest.approx(y0))
        assert moved


# ── Collision detection tests ─────────────────────────────────
class TestCollision:
    def test_bullet_hits_asteroid(self):
        from utils import circles_collide
        bullet_pos = pygame.Vector2(100, 100)
        asteroid_pos = pygame.Vector2(101, 100)
        assert circles_collide(bullet_pos, 3, asteroid_pos, 50) is True

    def test_bullet_misses_asteroid(self):
        from utils import circles_collide
        bullet_pos = pygame.Vector2(0, 0)
        asteroid_pos = pygame.Vector2(200, 200)
        assert circles_collide(bullet_pos, 3, asteroid_pos, 50) is False

    def test_ship_hits_asteroid(self):
        from utils import circles_collide
        from ship import PlayerShip
        ship = PlayerShip(100, 100)
        asteroid_pos = pygame.Vector2(105, 100)
        assert circles_collide(ship.pos, ship.RADIUS, asteroid_pos, 50) is True


# ── High score persistence tests ──────────────────────────────
class TestHighScore:
    def test_load_missing_file_returns_zero(self):
        from highscore import load_high_score
        import unittest.mock as mock
        with mock.patch("builtins.open", side_effect=FileNotFoundError):
            assert load_high_score() == 0

    def test_save_and_load_roundtrip(self):
        import highscore
        import unittest.mock as mock

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            tmp_path = f.name

        try:
            with mock.patch.object(highscore, "_SCORE_FILE", tmp_path):
                highscore.save_high_score(9999)
                result = highscore.load_high_score()
            assert result == 9999
        finally:
            os.unlink(tmp_path)

    def test_corrupt_json_returns_zero(self):
        from highscore import load_high_score
        import unittest.mock as mock
        import io
        with mock.patch("builtins.open", return_value=io.StringIO("NOT JSON")):
            assert load_high_score() == 0


# ── HUD tests ─────────────────────────────────────────────────
class TestHUD:
    def test_hud_draws_without_crash(self):
        from hud import HUD
        font = pygame.font.SysFont(None, 48)
        hud = HUD(font)
        screen = pygame.Surface((1280, 720))
        hud.draw(screen, score=1000, lives=3, wave=2, high_score=5000)

    def test_hud_accepts_zero_lives(self):
        from hud import HUD
        font = pygame.font.SysFont(None, 48)
        hud = HUD(font)
        screen = pygame.Surface((1280, 720))
        hud.draw(screen, score=0, lives=0, wave=1, high_score=0)


# ── Menu tests ────────────────────────────────────────────────
class TestMenu:
    def test_title_screen_draws(self):
        from menu import TitleScreen
        font = pygame.font.SysFont(None, 48)
        ts = TitleScreen(font)
        screen = pygame.Surface((1280, 720))
        ts.update(0.016)
        ts.draw(screen)

    def test_game_over_screen_draws(self):
        from menu import GameOverScreen
        font = pygame.font.SysFont(None, 48)
        go = GameOverScreen(font, score=2500, high_score=5000)
        screen = pygame.Surface((1280, 720))
        go.update(0.016)
        go.draw(screen)

    def test_game_over_new_record(self):
        from menu import GameOverScreen
        font = pygame.font.SysFont(None, 48)
        go = GameOverScreen(font, score=10000, high_score=9999)
        assert go._new_record is True


# ── SoundManager tests ────────────────────────────────────────
class TestSoundManager:
    def test_sound_manager_init_no_crash(self):
        from sounds import SoundManager
        sm = SoundManager()
        # Should not raise even with missing sound files
        sm.play("fire")
        sm.play("nonexistent_sound")

    def test_heartbeat_update_no_crash(self):
        from sounds import SoundManager
        sm = SoundManager()
        sm.update_heartbeat(0.016, asteroid_count=5)

    def test_stop_all_no_crash(self):
        from sounds import SoundManager
        sm = SoundManager()
        sm.stop_all()


# ── Settings constants completeness check ─────────────────────
class TestSettings:
    def test_all_required_constants_present(self):
        import settings
        required = [
            "SCREEN_WIDTH", "SCREEN_HEIGHT", "FPS",
            "DRAG_COEFFICIENT", "SHIP_THRUST", "MAX_SPEED", "ROTATION_SPEED",
            "BULLET_SPEED", "BULLET_LIFETIME", "MAX_BULLETS",
            "ASTEROID_LARGE_RADIUS", "ASTEROID_MEDIUM_RADIUS", "ASTEROID_SMALL_RADIUS",
            "ASTEROID_LARGE_SPEED_MIN", "ASTEROID_LARGE_SPEED_MAX",
            "ASTEROID_MEDIUM_SPEED_MIN", "ASTEROID_MEDIUM_SPEED_MAX",
            "ASTEROID_SMALL_SPEED_MIN", "ASTEROID_SMALL_SPEED_MAX",
            "ASTEROID_SPAWN_SAFE_RADIUS",
            "SCORE_LARGE_ASTEROID", "SCORE_MEDIUM_ASTEROID", "SCORE_SMALL_ASTEROID",
            "SCORE_LARGE_SAUCER", "SCORE_SMALL_SAUCER",
            "EXTRA_LIFE_THRESHOLD", "MAX_LIVES",
            "RESPAWN_DELAY", "INVINCIBILITY_TIME", "BLINK_RATE",
            "WAVE_ASTEROID_START", "WAVE_ASTEROID_MAX", "WAVE_TRANSITION_DELAY",
            "SAUCER_LARGE_RADIUS", "SAUCER_SMALL_RADIUS",
            "SAUCER_LARGE_FIRE_INTERVAL", "SAUCER_SMALL_FIRE_INTERVAL",
            "SAUCER_AIM_SPREAD", "SAUCER_SPAWN_INTERVAL_BASE", "SAUCER_SPAWN_INTERVAL_MIN",
            "SMALL_SAUCER_SCORE_THRESHOLD",
            "HYPERSPACE_DEATH_CHANCE", "HYPERSPACE_COOLDOWN",
            "WHITE", "BLACK", "LINE_WIDTH",
        ]
        for const in required:
            assert hasattr(settings, const), f"Missing constant: {const}"
