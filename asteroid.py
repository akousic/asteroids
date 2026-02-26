import math
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ASTEROID_LARGE_RADIUS, ASTEROID_MEDIUM_RADIUS, ASTEROID_SMALL_RADIUS,
    ASTEROID_LARGE_SPEED_MIN, ASTEROID_LARGE_SPEED_MAX,
    ASTEROID_MEDIUM_SPEED_MIN, ASTEROID_MEDIUM_SPEED_MAX,
    ASTEROID_SMALL_SPEED_MIN, ASTEROID_SMALL_SPEED_MAX,
    ASTEROID_SPAWN_SAFE_RADIUS,
    WHITE, LINE_WIDTH,
)
from utils import wrap_position


# Size configs: (radius, speed_min, speed_max, child_size)
_SIZE_CONFIG = {
    "large":  (ASTEROID_LARGE_RADIUS,  ASTEROID_LARGE_SPEED_MIN,  ASTEROID_LARGE_SPEED_MAX,  "medium"),
    "medium": (ASTEROID_MEDIUM_RADIUS, ASTEROID_MEDIUM_SPEED_MIN, ASTEROID_MEDIUM_SPEED_MAX, "small"),
    "small":  (ASTEROID_SMALL_RADIUS,  ASTEROID_SMALL_SPEED_MIN,  ASTEROID_SMALL_SPEED_MAX,  None),
}


def _make_polygon(radius: float, num_vertices: int = None) -> list:
    """Generate a jagged circle polygon with ±30% radius variation."""
    if num_vertices is None:
        num_vertices = random.randint(8, 12)
    points = []
    for i in range(num_vertices):
        angle = (2 * math.pi * i) / num_vertices
        r = radius * random.uniform(0.7, 1.3)
        points.append((math.cos(angle) * r, math.sin(angle) * r))
    return points


def _random_edge_pos(ship_pos: pygame.Vector2) -> pygame.Vector2:
    """Spawn at a random screen edge, away from the ship."""
    for _ in range(20):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            pos = pygame.Vector2(random.uniform(0, SCREEN_WIDTH), 0)
        elif edge == "bottom":
            pos = pygame.Vector2(random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT)
        elif edge == "left":
            pos = pygame.Vector2(0, random.uniform(0, SCREEN_HEIGHT))
        else:
            pos = pygame.Vector2(SCREEN_WIDTH, random.uniform(0, SCREEN_HEIGHT))
        if pos.distance_to(ship_pos) >= ASTEROID_SPAWN_SAFE_RADIUS:
            return pos
    # Fallback: corner
    return pygame.Vector2(0, 0)


class Asteroid:
    """An asteroid with procedural polygon, constant velocity, and screen wrapping."""

    def __init__(
        self,
        pos: pygame.Vector2,
        vel: pygame.Vector2,
        size: str,
    ) -> None:
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.size = size
        self.radius = _SIZE_CONFIG[size][0]
        self._polygon = _make_polygon(self.radius)
        self._rotation = 0.0
        self._rotation_speed = random.uniform(-60, 60)  # degrees/s

    @classmethod
    def spawn_large(cls, ship_pos: pygame.Vector2) -> "Asteroid":
        """Spawn a large asteroid at a random screen edge."""
        pos = _random_edge_pos(ship_pos)
        speed = random.uniform(ASTEROID_LARGE_SPEED_MIN, ASTEROID_LARGE_SPEED_MAX)
        angle = random.uniform(0, 2 * math.pi)
        vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        return cls(pos, vel, "large")

    def split(self) -> list:
        """Return child asteroids when this one is destroyed. Small → no children."""
        child_size = _SIZE_CONFIG[self.size][3]
        if child_size is None:
            return []
        cfg = _SIZE_CONFIG[child_size]
        children = []
        for _ in range(2):
            speed = random.uniform(cfg[1], cfg[2])
            angle = random.uniform(0, 2 * math.pi)
            vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            children.append(Asteroid(self.pos, vel, child_size))
        return children

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt
        self.pos = wrap_position(self.pos, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._rotation += self._rotation_speed * dt

    def draw(self, screen: pygame.Surface) -> None:
        import math as _math
        angle = _math.radians(self._rotation)
        cos_a, sin_a = _math.cos(angle), _math.sin(angle)
        world_pts = []
        for x, y in self._polygon:
            rx = x * cos_a - y * sin_a
            ry = x * sin_a + y * cos_a
            world_pts.append((self.pos.x + rx, self.pos.y + ry))
        pygame.draw.polygon(screen, WHITE, world_pts, LINE_WIDTH)
