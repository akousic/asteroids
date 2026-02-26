import math
import random
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from utils import wrap_position


class ExplosionParticle:
    """A single short-lived line segment that flies outward from an explosion."""

    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(pos)
        speed = random.uniform(60, 220)
        angle = random.uniform(0, 2 * math.pi)
        self.vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self._lifetime = random.uniform(0.4, 1.2)
        self._max_lifetime = self._lifetime
        self.expired = False
        # Each particle is a short line segment
        length = random.uniform(4, 12)
        self._end_offset = pygame.Vector2(math.cos(angle) * length, math.sin(angle) * length)

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt
        self.pos = wrap_position(self.pos, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.vel *= 0.95  # slight drag
        self._lifetime -= dt
        if self._lifetime <= 0:
            self.expired = True

    def draw(self, screen: pygame.Surface) -> None:
        # Fade out: alpha proportional to remaining lifetime
        alpha = max(0, int(255 * (self._lifetime / self._max_lifetime)))
        color = (alpha, alpha, alpha)
        end = self.pos + self._end_offset
        pygame.draw.line(screen, color, (int(self.pos.x), int(self.pos.y)),
                         (int(end.x), int(end.y)), 1)
