import math
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    SAUCER_LARGE_RADIUS, SAUCER_SMALL_RADIUS,
    SAUCER_LARGE_FIRE_INTERVAL, SAUCER_SMALL_FIRE_INTERVAL,
    SAUCER_AIM_SPREAD,
    WHITE, LINE_WIDTH,
    SMALL_SAUCER_SCORE_THRESHOLD,
)
from utils import wrap_position


# Saucer polygon: classic flying-saucer silhouette in local space
_SAUCER_BODY = [
    (-1.0, 0.0),   # left middle
    (-0.6, -0.4),  # upper-left
    (0.6, -0.4),   # upper-right
    (1.0, 0.0),    # right middle
    (0.6, 0.4),    # lower-right
    (-0.6, 0.4),   # lower-left
]
_SAUCER_DOME = [
    (-0.4, -0.4),
    (-0.2, -0.75),
    (0.2, -0.75),
    (0.4, -0.4),
]


class Saucer:
    """Enemy saucer — large aims randomly, small aims at player."""

    def __init__(self, large: bool = True) -> None:
        self.large = large
        self.radius = SAUCER_LARGE_RADIUS if large else SAUCER_SMALL_RADIUS
        self._fire_interval = SAUCER_LARGE_FIRE_INTERVAL if large else SAUCER_SMALL_FIRE_INTERVAL
        self._fire_timer = self._fire_interval
        self._wants_to_fire = False
        self.expired = False

        # Spawn on left or right edge
        side = random.choice([-1, 1])
        self.pos = pygame.Vector2(
            0 if side == -1 else SCREEN_WIDTH,
            random.uniform(SCREEN_HEIGHT * 0.2, SCREEN_HEIGHT * 0.8),
        )
        speed = 120 if large else 160
        self.vel = pygame.Vector2(speed * side, 0)

        # Direction change timer
        self._dir_timer = random.uniform(1.5, 3.0)

        # Lifespan (leave screen = expired)
        self._off_screen_timer = 0.0

    def update(self, dt: float, ship) -> None:
        self.pos += self.vel * dt

        # Wrap vertically, expire horizontally
        self.pos.y = self.pos.y % SCREEN_HEIGHT
        if self.pos.x < -self.radius * 2 or self.pos.x > SCREEN_WIDTH + self.radius * 2:
            self.expired = True
            return

        # Random vertical direction changes
        self._dir_timer -= dt
        if self._dir_timer <= 0:
            vy = random.choice([-1, 0, 1]) * (80 if self.large else 100)
            self.vel.y = vy
            self._dir_timer = random.uniform(1.5, 3.0)

        # Firing
        self._fire_timer -= dt
        if self._fire_timer <= 0:
            self._fire_timer = self._fire_interval
            self._wants_to_fire = True
        else:
            self._wants_to_fire = False

    def wants_to_fire(self) -> bool:
        return self._wants_to_fire

    def create_bullet(self, BulletClass, ship) -> object:
        """Create a bullet aimed at the ship (small saucer) or random (large)."""
        if self.large or ship is None or not ship.alive:
            angle_rad = random.uniform(0, 2 * math.pi)
        else:
            # Aim at ship with spread
            dx = ship.pos.x - self.pos.x
            dy = ship.pos.y - self.pos.y
            angle_rad = math.atan2(dx, -dy)  # convert to our angle convention
            spread = math.radians(random.uniform(-SAUCER_AIM_SPREAD, SAUCER_AIM_SPREAD))
            angle_rad += spread

        angle_deg = math.degrees(angle_rad)
        dummy_vel = pygame.Vector2(0, 0)
        return BulletClass(self.pos, angle_deg, dummy_vel, is_player_bullet=False)

    def draw(self, screen: pygame.Surface) -> None:
        r = self.radius
        # Scale body points by radius
        body = [(self.pos.x + x * r, self.pos.y + y * r) for x, y in _SAUCER_BODY]
        pygame.draw.polygon(screen, WHITE, body, LINE_WIDTH)
        dome = [(self.pos.x + x * r, self.pos.y + y * r) for x, y in _SAUCER_DOME]
        pygame.draw.polygon(screen, WHITE, dome, LINE_WIDTH)
