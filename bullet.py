import math
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BULLET_SPEED, BULLET_LIFETIME,
    WHITE,
)
from utils import wrap_position


class Bullet:
    """A projectile fired by the player ship or a saucer."""

    def __init__(
        self,
        pos: pygame.Vector2,
        angle: float,
        ship_vel: pygame.Vector2,
        is_player_bullet: bool = True,
    ) -> None:
        self.pos = pygame.Vector2(pos)
        self.is_player_bullet = is_player_bullet
        self.expired = False
        self._lifetime = BULLET_LIFETIME

        rad = math.radians(angle)
        direction = pygame.Vector2(math.sin(rad), -math.cos(rad))
        # Player bullets inherit ship velocity
        if is_player_bullet:
            self.vel = direction * BULLET_SPEED + ship_vel
        else:
            self.vel = direction * BULLET_SPEED

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt
        self.pos = wrap_position(self.pos, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._lifetime -= dt
        if self._lifetime <= 0:
            self.expired = True

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), 2)
