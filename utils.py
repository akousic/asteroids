import math
import pygame


def wrap_position(pos: pygame.Vector2, width: int, height: int) -> pygame.Vector2:
    """Wrap a position to stay within screen bounds (torus topology)."""
    return pygame.Vector2(pos.x % width, pos.y % height)


def circles_collide(
    pos_a: pygame.Vector2, radius_a: float,
    pos_b: pygame.Vector2, radius_b: float,
) -> bool:
    """Return True if two circles overlap."""
    return pos_a.distance_to(pos_b) < (radius_a + radius_b)


def rotate_points(points: list, angle_degrees: float) -> list:
    """Rotate a list of (x, y) points around the origin by angle_degrees."""
    angle = math.radians(angle_degrees)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        (x * cos_a - y * sin_a, x * sin_a + y * cos_a)
        for x, y in points
    ]
