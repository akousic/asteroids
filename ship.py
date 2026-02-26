import math
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    SHIP_THRUST, MAX_SPEED, DRAG_COEFFICIENT, ROTATION_SPEED,
    WHITE, LINE_WIDTH,
    INVINCIBILITY_TIME, BLINK_RATE,
    HYPERSPACE_DEATH_CHANCE, HYPERSPACE_COOLDOWN,
)
from utils import wrap_position, rotate_points


# Ship polygon defined in local space (nose pointing up, i.e. +Y in screen coords is down)
# We store as (x, y) with nose at (0, -20), wings at (±12, 10), tail notch at (0, 5)
_SHIP_POINTS = [
    (0, -20),    # nose
    (12, 10),    # right wing tip
    (0, 5),      # tail notch (inner)
    (-12, 10),   # left wing tip
]

_THRUSTER_FLAME = [
    (0, 5),      # inner notch (same as tail notch)
    (5, 14),     # right flame base
    (0, 22),     # flame tip
    (-5, 14),    # left flame base
]


class PlayerShip:
    """Player-controlled ship with Newtonian physics."""

    RADIUS = 14  # collision radius in px

    def __init__(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0.0          # degrees; 0 = nose up (−Y axis)
        self.alive = True
        self.invincible = False
        self.invincibility_timer = 0.0
        self._blink_frame = 0
        self._show = True         # for blinking during invincibility
        self._thrust_on = False   # draw flame only when thrusting
        self._hyperspace_cooldown = 0.0
        self._flame_toggle = 0    # flicker counter for thrust flame

    # ── Input ─────────────────────────────────────────────────
    def handle_keys(self, keys, dt: float) -> None:
        """Read held keys and apply thrust / rotation."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= ROTATION_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += ROTATION_SPEED * dt

        self._thrust_on = keys[pygame.K_UP] or keys[pygame.K_w]
        if self._thrust_on:
            # Direction: angle=0 means nose points up (−Y), so thrust vector is:
            rad = math.radians(self.angle)
            thrust_dir = pygame.Vector2(math.sin(rad), -math.cos(rad))
            self.vel += thrust_dir * SHIP_THRUST * dt

    # ── Update ────────────────────────────────────────────────
    def update(self, dt: float) -> None:
        # Apply drag
        self.vel *= DRAG_COEFFICIENT

        # Cap speed
        speed = self.vel.length()
        if speed > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        # Move
        self.pos += self.vel * dt

        # Wrap
        self.pos = wrap_position(self.pos, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Invincibility countdown
        if self.invincible:
            self.invincibility_timer -= dt
            self._blink_frame += 1
            if self._blink_frame % BLINK_RATE == 0:
                self._show = not self._show
            if self.invincibility_timer <= 0:
                self.invincible = False
                self._show = True

        # Hyperspace cooldown
        if self._hyperspace_cooldown > 0:
            self._hyperspace_cooldown -= dt

        # Flame flicker
        if self._thrust_on:
            self._flame_toggle = (self._flame_toggle + 1) % 4

    # ── Hyperspace ────────────────────────────────────────────
    def hyperspace(self) -> bool:
        """Teleport to a random position. Returns True if ship survives."""
        import random
        if self._hyperspace_cooldown > 0:
            return True  # nothing happens during cooldown
        self._hyperspace_cooldown = HYPERSPACE_COOLDOWN
        if random.random() < HYPERSPACE_DEATH_CHANCE:
            self.alive = False
            return False
        self.pos = pygame.Vector2(
            random.uniform(0, SCREEN_WIDTH),
            random.uniform(0, SCREEN_HEIGHT),
        )
        self.vel = pygame.Vector2(0, 0)
        return True

    # ── Respawn ───────────────────────────────────────────────
    def respawn(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0.0
        self.alive = True
        self.invincible = True
        self.invincibility_timer = INVINCIBILITY_TIME
        self._blink_frame = 0
        self._show = True
        self._hyperspace_cooldown = 0.0

    # ── Draw ──────────────────────────────────────────────────
    def draw(self, screen: pygame.Surface) -> None:
        if not self._show:
            return

        rotated = rotate_points(_SHIP_POINTS, self.angle)
        world_pts = [(self.pos.x + x, self.pos.y + y) for x, y in rotated]
        pygame.draw.polygon(screen, WHITE, world_pts, LINE_WIDTH)

        if self._thrust_on and self._flame_toggle < 3:  # flicker: skip every 4th frame
            flame_pts = rotate_points(_THRUSTER_FLAME, self.angle)
            world_flame = [(self.pos.x + x, self.pos.y + y) for x, y in flame_pts]
            pygame.draw.polygon(screen, WHITE, world_flame, LINE_WIDTH)
