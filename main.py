import sys
import random
import pygame
from enum import Enum, auto
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK,
    MAX_BULLETS, RESPAWN_DELAY, RESPAWN_SAFE_RADIUS,
    WAVE_ASTEROID_START, WAVE_ASTEROID_MAX, WAVE_TRANSITION_DELAY,
    EXTRA_LIFE_THRESHOLD, MAX_LIVES,
    SCORE_LARGE_ASTEROID, SCORE_MEDIUM_ASTEROID, SCORE_SMALL_ASTEROID,
    SCORE_LARGE_SAUCER, SCORE_SMALL_SAUCER,
    SAUCER_SPAWN_INTERVAL_BASE, SAUCER_SPAWN_INTERVAL_MIN,
)
from game_config import SettingsManager
from settings_overlay import SettingsOverlay


class GameState(Enum):
    TITLE_SCREEN = auto()
    PLAYING      = auto()
    PAUSED       = auto()
    SETTINGS     = auto()
    GAME_OVER    = auto()


class PlaySubState(Enum):
    ACTIVE          = auto()
    RESPAWNING      = auto()
    WAVE_TRANSITION = auto()


# ── Lazy imports (modules created in later stories) ───────────
def _import_ship():
    from ship import PlayerShip
    return PlayerShip

def _import_bullet():
    from bullet import Bullet
    return Bullet

def _import_asteroid():
    from asteroid import Asteroid
    return Asteroid

def _import_saucer():
    from saucer import Saucer
    return Saucer

def _import_particle():
    from particle import ExplosionParticle
    return ExplosionParticle

def _import_hud():
    from hud import HUD
    return HUD

def _import_menu():
    from menu import TitleScreen, GameOverScreen
    return TitleScreen, GameOverScreen

def _import_highscore():
    from highscore import load_high_score, save_high_score
    return load_high_score, save_high_score

def _import_sounds():
    from sounds import SoundManager
    return SoundManager


# ── Module-level state ────────────────────────────────────────
running        = True
state          = GameState.TITLE_SCREEN
play_sub_state = PlaySubState.ACTIVE
_font          = None   # initialized after pygame.init()

# Game objects (populated during PLAYING)
ship           = None
bullets        = []
asteroids      = []
saucers        = []
particles      = []

# Game stats
score          = 0
lives          = 3
wave           = 1
high_score     = 0

# Timers
_respawn_timer    = 0.0
_wave_timer       = 0.0
_saucer_timer     = 0.0

# UI objects (lazy-imported)
_hud           = None
_title_screen  = None
_game_over_screen = None
_sound_manager = None
_settings_mgr  = SettingsManager()
_settings_overlay = None
_settings_return_state = GameState.TITLE_SCREEN
_bindings = _settings_mgr.key_bindings()
_paused_index = 0
_PAUSED_OPTIONS = ["Resume", "Restart", "Settings", "Fullscreen", "Quit"]

_controller_status_timer = 0.0
_controller_status_msg = ""


# ── State transition ──────────────────────────────────────────
def transition_to(new_state: GameState) -> None:
    global state
    state = new_state
    _entry_hooks = {
        GameState.TITLE_SCREEN: _on_enter_title,
        GameState.PLAYING:      _on_enter_playing,
        GameState.PAUSED:       _on_enter_paused,
        GameState.SETTINGS:     _on_enter_settings,
        GameState.GAME_OVER:    _on_enter_game_over,
    }
    hook = _entry_hooks.get(new_state)
    if hook:
        hook()


def _on_enter_title() -> None:
    global _title_screen
    try:
        TitleScreen, _ = _import_menu()
        _title_screen = TitleScreen(_font)
    except Exception:
        _title_screen = None


def _on_enter_playing() -> None:
    global ship, bullets, asteroids, saucers, particles
    global score, lives, wave, high_score
    global _respawn_timer, _wave_timer, _saucer_timer
    global play_sub_state, _hud, _sound_manager, _bindings

    # Load high score
    try:
        load_high_score, _ = _import_highscore()
        high_score = load_high_score()
    except Exception:
        high_score = 0

    # Create HUD
    try:
        HUD = _import_hud()
        _hud = HUD(_font)
    except Exception:
        _hud = None

    # Create sound manager
    try:
        SoundManager = _import_sounds()
        _sound_manager = SoundManager()
    except Exception:
        _sound_manager = None

    _apply_runtime_settings()

    score = 0
    lives = MAX_LIVES
    wave  = 1
    bullets = []
    saucers = []
    particles = []
    _respawn_timer = 0.0
    _saucer_timer  = SAUCER_SPAWN_INTERVAL_BASE
    play_sub_state = PlaySubState.ACTIVE

    # Create ship
    PlayerShip = _import_ship()
    ship = PlayerShip(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ship.invincible = True
    ship.invincibility_timer = 3.0

    # Spawn first wave
    _spawn_wave(wave)


def _apply_runtime_settings() -> None:
    global _bindings
    _bindings = _settings_mgr.key_bindings()
    if _sound_manager:
        a = _settings_mgr.settings["audio"]
        _sound_manager.set_volumes(a.get("master", 0.8), a.get("music", 0.6), a.get("sfx", 0.9))


def _toggle_fullscreen() -> None:
    global _is_fullscreen
    _is_fullscreen = not _is_fullscreen
    _apply_display_mode()


def _update_controller_status(msg: str, seconds: float = 2.5) -> None:
    global _controller_status_msg, _controller_status_timer
    _controller_status_msg = msg
    _controller_status_timer = max(_controller_status_timer, seconds)


def _get_gamepad():
    if pygame.joystick.get_count() <= 0:
        return None
    try:
        js = pygame.joystick.Joystick(0)
        if not js.get_init():
            js.init()
        return js
    except Exception:
        return None


def _apply_gamepad_input(dt: float) -> None:
    global bullets
    if game_state != GameState.PLAYING or play_sub_state != PlaySubState.ACTIVE:
        return
    if not ship.alive:
        return

    js = _get_gamepad()
    if js is None:
        return

    # Left stick X for turning, deadzone
    axis_x = js.get_axis(0)
    deadzone = 0.2
    if abs(axis_x) >= deadzone:
        ship.angle += axis_x * ROTATION_SPEED * dt

    # A (0) = thrust
    thrust = js.get_button(0)
    ship._thrust_on = bool(thrust)

    # Start/Menu button pauses
    pause_pressed = False
    try:
        pause_pressed = bool(js.get_button(7))
    except Exception:
        pause_pressed = False

    if pause_pressed:
        if not hasattr(_apply_gamepad_input, "_last_pause"):
            _apply_gamepad_input._last_pause = 0.0
        now = pygame.time.get_ticks() / 1000.0
        if now - _apply_gamepad_input._last_pause > 0.25:
            transition_to(GameState.PAUSED)
            _apply_gamepad_input._last_pause = now
            return

    # RT axis (5) or B (1) as fire
    fire_pressed = False
    try:
        rt = js.get_axis(5)  # ranges -1..1
        fire_pressed = rt > 0.5
    except Exception:
        pass
    fire_pressed = fire_pressed or bool(js.get_button(1))

    if fire_pressed and len(bullets) < MAX_BULLETS:
        if not hasattr(_apply_gamepad_input, "_last_fire"):
            _apply_gamepad_input._last_fire = 0.0
        now = pygame.time.get_ticks() / 1000.0
        if now - _apply_gamepad_input._last_fire > 0.16:
            bullets.append(Bullet(ship.x, ship.y, ship.angle))
            _apply_gamepad_input._last_fire = now


def _on_enter_paused() -> None:
    global _paused_index
    _paused_index = 0


def _on_enter_settings() -> None:
    global _settings_overlay
    _settings_overlay = SettingsOverlay(_settings_mgr)


def _on_enter_game_over() -> None:
    global _game_over_screen, high_score
    # Save high score
    try:
        load_high_score, save_high_score = _import_highscore()
        if score > high_score:
            high_score = score
            save_high_score(high_score)
    except Exception:
        pass

    try:
        _, GameOverScreen = _import_menu()
        _game_over_screen = GameOverScreen(_font, score, high_score)
    except Exception:
        _game_over_screen = None


# ── Wave management ───────────────────────────────────────────
def _spawn_wave(wave_num: int) -> None:
    """Spawn large asteroids for the given wave number."""
    global asteroids
    Asteroid = _import_asteroid()
    count = min(WAVE_ASTEROID_START + wave_num - 1, WAVE_ASTEROID_MAX)
    asteroids = []
    ship_pos = ship.pos if ship else pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    for _ in range(count):
        asteroids.append(Asteroid.spawn_large(ship_pos))


def _next_wave() -> None:
    global wave, play_sub_state, _wave_timer, asteroids, saucers, particles
    wave += 1
    saucers = []
    particles = []
    _spawn_wave(wave)
    play_sub_state = PlaySubState.ACTIVE
    # Give ship brief invincibility at wave start
    if ship and ship.alive:
        ship.invincible = True
        ship.invincibility_timer = 2.0


# ── Scoring ───────────────────────────────────────────────────
_next_extra_life_threshold = EXTRA_LIFE_THRESHOLD

def _add_score(points: int) -> None:
    global score, lives, _next_extra_life_threshold
    score += points
    if score >= _next_extra_life_threshold:
        lives = min(lives + 1, MAX_LIVES)
        _next_extra_life_threshold += EXTRA_LIFE_THRESHOLD
        if _sound_manager:
            _sound_manager.play("extra_life")


# ── Event handling ────────────────────────────────────────────
def handle_events() -> None:
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            return
        if event.type == pygame.KEYDOWN:
            if state == GameState.TITLE_SCREEN:
                _handle_title_events(event)
            elif state == GameState.PLAYING:
                _handle_playing_events(event)
            elif state == GameState.PAUSED:
                _handle_paused_events(event)
            elif state == GameState.GAME_OVER:
                _handle_game_over_events(event)


def _handle_title_events(event) -> None:
    global running, _settings_return_state
    if event.key == pygame.K_ESCAPE:
        running = False
    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
        global _next_extra_life_threshold
        _next_extra_life_threshold = EXTRA_LIFE_THRESHOLD
        transition_to(GameState.PLAYING)
    elif event.key == pygame.K_s:
        _settings_return_state = GameState.TITLE_SCREEN
        transition_to(GameState.SETTINGS)
    elif event.key == pygame.K_f:
        _toggle_fullscreen()


def _handle_playing_events(event) -> None:
    global bullets, play_sub_state
    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
        transition_to(GameState.PAUSED)
    elif event.key == pygame.K_SPACE:
        _fire_bullet()
    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
        _do_hyperspace()


def _handle_paused_events(event) -> None:
    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
        transition_to(GameState.PLAYING)


def _handle_game_over_events(event) -> None:
    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
        transition_to(GameState.TITLE_SCREEN)


def _fire_bullet() -> None:
    """Fire a bullet from the ship nose if under MAX_BULLETS limit."""
    import math
    if not ship or not ship.alive:
        return
    if play_sub_state != PlaySubState.ACTIVE:
        return
    if len(bullets) >= MAX_BULLETS:
        return
    try:
        Bullet = _import_bullet()
        rad = math.radians(ship.angle)
        nose_offset = pygame.Vector2(math.sin(rad) * 20, -math.cos(rad) * 20)
        bullet = Bullet(ship.pos + nose_offset, ship.angle, ship.vel)
        bullets.append(bullet)
        if _sound_manager:
            _sound_manager.play("fire")
    except Exception:
        pass


def _do_hyperspace() -> None:
    if not ship or not ship.alive:
        return
    if play_sub_state != PlaySubState.ACTIVE:
        return
    survived = ship.hyperspace()
    if not survived:
        _on_ship_destroyed()
    elif _sound_manager:
        _sound_manager.play("hyperspace")


# ── Update ────────────────────────────────────────────────────
def update(dt: float) -> None:
    if state == GameState.TITLE_SCREEN:
        _update_title(dt)
    elif state == GameState.PLAYING:
        _update_playing(dt)
    elif state == GameState.PAUSED:
        _update_paused(dt)
    elif state == GameState.GAME_OVER:
        _update_game_over(dt)


def _update_title(dt: float) -> None:
    if _title_screen:
        _title_screen.update(dt)


def _update_playing(dt: float) -> None:
    global play_sub_state, _respawn_timer, _wave_timer, _saucer_timer

    if play_sub_state == PlaySubState.ACTIVE:
        _update_active(dt)
    elif play_sub_state == PlaySubState.RESPAWNING:
        _respawn_timer -= dt
        if _respawn_timer <= 0:
            _do_respawn()
    elif play_sub_state == PlaySubState.WAVE_TRANSITION:
        _wave_timer -= dt
        if _wave_timer <= 0:
            _next_wave()


def _update_active(dt: float) -> None:
    global bullets, asteroids, saucers, particles, _saucer_timer

    # Ship
    if ship and ship.alive:
        keys = pygame.key.get_pressed()
        ship.handle_keys(keys, dt, _bindings)
        ship.update(dt)

    # Bullets
    for b in bullets[:]:
        b.update(dt)
        if b.expired:
            bullets.remove(b)

    # Asteroids
    for a in asteroids:
        a.update(dt)

    # Saucers
    for s in saucers[:]:
        s.update(dt, ship)
        if s.expired:
            saucers.remove(s)
        elif s.wants_to_fire():
            _fire_saucer_bullet(s)

    # Particles
    for p in particles[:]:
        p.update(dt)
        if p.expired:
            particles.remove(p)

    # Saucer spawning
    _saucer_timer -= dt
    if _saucer_timer <= 0:
        _spawn_saucer()
        _saucer_timer = max(
            SAUCER_SPAWN_INTERVAL_BASE - (wave - 1) * 1.0,
            SAUCER_SPAWN_INTERVAL_MIN,
        )

    # Heartbeat audio
    if _sound_manager:
        _sound_manager.update_heartbeat(dt, len(asteroids))

    # Collisions
    _check_collisions()

    # Wave clear check
    if not asteroids and not saucers and play_sub_state == PlaySubState.ACTIVE:
        global _wave_timer
        _wave_timer = WAVE_TRANSITION_DELAY
        play_sub_state = PlaySubState.WAVE_TRANSITION


def _spawn_saucer() -> None:
    try:
        Saucer = _import_saucer()
        large = score < 40000  # SMALL_SAUCER_SCORE_THRESHOLD
        saucer = Saucer(large=large)
        saucers.append(saucer)
        if _sound_manager:
            _sound_manager.play("saucer_large" if large else "saucer_small")
    except Exception:
        pass


def _fire_saucer_bullet(saucer) -> None:
    try:
        Bullet = _import_bullet()
        b = saucer.create_bullet(Bullet, ship)
        if b:
            bullets.append(b)
    except Exception:
        pass


# ── Collision detection ───────────────────────────────────────
def _check_collisions() -> None:
    from utils import circles_collide

    # Bullet vs asteroid
    for b in bullets[:]:
        if b.is_player_bullet:
            for a in asteroids[:]:
                if circles_collide(b.pos, 3, a.pos, a.radius):
                    _on_bullet_hit_asteroid(b, a)
                    if b in bullets:
                        bullets.remove(b)
                    break
        else:
            # Saucer bullet vs player
            if ship and ship.alive and not ship.invincible:
                if circles_collide(b.pos, 3, ship.pos, ship.RADIUS):
                    if b in bullets:
                        bullets.remove(b)
                    _on_ship_destroyed()

    # Bullet vs saucer
    for b in bullets[:]:
        if b.is_player_bullet:
            for s in saucers[:]:
                if circles_collide(b.pos, 3, s.pos, s.radius):
                    _on_bullet_hit_saucer(b, s)
                    if b in bullets:
                        bullets.remove(b)
                    break

    # Ship vs asteroid
    if ship and ship.alive and not ship.invincible:
        for a in asteroids[:]:
            if circles_collide(ship.pos, ship.RADIUS, a.pos, a.radius):
                _on_ship_hit_asteroid(a)
                break

    # Ship vs saucer
    if ship and ship.alive and not ship.invincible:
        for s in saucers[:]:
            if circles_collide(ship.pos, ship.RADIUS, s.pos, s.radius):
                saucers.remove(s)
                _on_ship_destroyed()
                break


def _on_bullet_hit_asteroid(bullet, asteroid) -> None:
    """Handle bullet hitting an asteroid: split, score, particles."""
    asteroids.remove(asteroid)
    # Score
    if asteroid.size == "large":
        _add_score(SCORE_LARGE_ASTEROID)
    elif asteroid.size == "medium":
        _add_score(SCORE_MEDIUM_ASTEROID)
    elif asteroid.size == "small":
        _add_score(SCORE_SMALL_ASTEROID)

    # Split
    children = asteroid.split()
    asteroids.extend(children)

    # Explosion
    _spawn_explosion(asteroid.pos)
    if _sound_manager:
        _sound_manager.play("explosion_asteroid")


def _on_bullet_hit_saucer(bullet, saucer) -> None:
    saucers.remove(saucer)
    if saucer.large:
        _add_score(SCORE_LARGE_SAUCER)
    else:
        _add_score(SCORE_SMALL_SAUCER)
    _spawn_explosion(saucer.pos)
    if _sound_manager:
        _sound_manager.play("explosion_saucer")


def _on_ship_hit_asteroid(asteroid) -> None:
    asteroids.remove(asteroid)
    children = asteroid.split()
    asteroids.extend(children)
    _spawn_explosion(asteroid.pos)
    _on_ship_destroyed()


def _on_ship_destroyed() -> None:
    global lives, play_sub_state, _respawn_timer
    if ship:
        ship.alive = False
        _spawn_explosion(ship.pos)
    if _sound_manager:
        _sound_manager.play("explosion_ship")
    lives -= 1
    if lives <= 0:
        transition_to(GameState.GAME_OVER)
    else:
        play_sub_state = PlaySubState.RESPAWNING
        _respawn_timer = RESPAWN_DELAY


def _do_respawn() -> None:
    global play_sub_state
    if ship:
        ship.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    play_sub_state = PlaySubState.ACTIVE


def _spawn_explosion(pos: pygame.Vector2) -> None:
    try:
        ExplosionParticle = _import_particle()
        for _ in range(12):
            particles.append(ExplosionParticle(pos))
    except Exception:
        pass


def _update_paused(dt: float) -> None:
    pass


def _update_game_over(dt: float) -> None:
    if _game_over_screen:
        _game_over_screen.update(dt)


# ── Draw ──────────────────────────────────────────────────────
def draw(screen: pygame.Surface) -> None:
    screen.fill(BLACK)
    if state == GameState.TITLE_SCREEN:
        _draw_title(screen)
    elif state == GameState.PLAYING:
        _draw_playing(screen)
    elif state == GameState.PAUSED:
        _draw_paused(screen)
    elif state == GameState.GAME_OVER:
        _draw_game_over(screen)


def _draw_centered(screen: pygame.Surface, text: str, y_offset: int = 0) -> None:
    surf = _font.render(text, True, WHITE)
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surf, rect)


def _draw_title(screen: pygame.Surface) -> None:
    if _title_screen:
        _title_screen.draw(screen)
    else:
        _draw_centered(screen, "ASTEROIDS")
        small = pygame.font.SysFont(None, 32)
        surf = small.render("Press ENTER or SPACE to play", True, WHITE)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(surf, rect)


def _draw_playing(screen: pygame.Surface) -> None:
    # Draw game objects
    for p in particles:
        p.draw(screen)
    for a in asteroids:
        a.draw(screen)
    for b in bullets:
        b.draw(screen)
    for s in saucers:
        s.draw(screen)
    if ship and ship.alive:
        ship.draw(screen)

    # Draw HUD
    if _hud:
        _hud.draw(screen, score, lives, wave, high_score)
    else:
        _draw_fallback_hud(screen)

    # Wave transition overlay
    if play_sub_state == PlaySubState.WAVE_TRANSITION:
        _draw_centered(screen, f"WAVE {wave + 1}", -30)
    elif play_sub_state == PlaySubState.RESPAWNING:
        _draw_centered(screen, "SHIP DESTROYED", -30)


def _draw_fallback_hud(screen: pygame.Surface) -> None:
    """Minimal score/lives display used before hud.py exists."""
    surf = _font.render(f"SCORE: {score}   LIVES: {lives}   WAVE: {wave}", True, WHITE)
    screen.blit(surf, (10, 10))


def _draw_paused(screen: pygame.Surface) -> None:
    # Draw the game state underneath
    for a in asteroids:
        a.draw(screen)
    for b in bullets:
        b.draw(screen)
    if ship and ship.alive:
        ship.draw(screen)
    # Overlay
    _draw_centered(screen, "PAUSED")
    small = pygame.font.SysFont(None, 32)
    surf = small.render("Press ESC or P to resume", True, WHITE)
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(surf, rect)


def _draw_game_over(screen: pygame.Surface) -> None:
    if _game_over_screen:
        _game_over_screen.draw(screen)
    else:
        _draw_centered(screen, "GAME OVER", -40)
        small = pygame.font.SysFont(None, 36)
        surf = small.render(f"Score: {score}   High Score: {high_score}", True, WHITE)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        screen.blit(surf, rect)
        surf2 = small.render("Press ENTER or SPACE", True, WHITE)
        rect2 = surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 55))
        screen.blit(surf2, rect2)


# ── Main ──────────────────────────────────────────────────────
def main() -> None:
    global running, _font

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock  = pygame.time.Clock()
    _font  = pygame.font.SysFont(None, 48)

    running = True
    transition_to(GameState.TITLE_SCREEN)

    while running:
        dt = clock.tick(FPS) / 1000.0

        handle_events()
        update(dt)
        draw(screen)
        # Controller status hint
        if _controller_status_timer > 0:
            font = pygame.font.SysFont(None, 28)
            txt = font.render(_controller_status_msg, True, (180, 220, 255))
            screen.blit(txt, (SCREEN_WIDTH - txt.get_width() - 16, 12))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
