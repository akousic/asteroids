import math
import sys
import os

# Allow importing from parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import pytest
from utils import wrap_position, circles_collide, rotate_points


# ── wrap_position ─────────────────────────────────────────────
class TestWrapPosition:
    def test_no_wrap_needed(self):
        pos = pygame.Vector2(100, 200)
        result = wrap_position(pos, 1280, 720)
        assert result.x == pytest.approx(100)
        assert result.y == pytest.approx(200)

    def test_wrap_right_edge(self):
        pos = pygame.Vector2(1280, 360)
        result = wrap_position(pos, 1280, 720)
        assert result.x == pytest.approx(0)
        assert result.y == pytest.approx(360)

    def test_wrap_beyond_right(self):
        pos = pygame.Vector2(1300, 360)
        result = wrap_position(pos, 1280, 720)
        assert result.x == pytest.approx(20)

    def test_wrap_bottom_edge(self):
        pos = pygame.Vector2(640, 720)
        result = wrap_position(pos, 1280, 720)
        assert result.y == pytest.approx(0)

    def test_wrap_negative_x(self):
        pos = pygame.Vector2(-10, 360)
        result = wrap_position(pos, 1280, 720)
        assert result.x == pytest.approx(1270)

    def test_wrap_negative_y(self):
        pos = pygame.Vector2(640, -5)
        result = wrap_position(pos, 1280, 720)
        assert result.y == pytest.approx(715)

    def test_returns_vector2(self):
        pos = pygame.Vector2(0, 0)
        result = wrap_position(pos, 1280, 720)
        assert isinstance(result, pygame.Vector2)


# ── circles_collide ───────────────────────────────────────────
class TestCirclesCollide:
    def test_overlapping_circles(self):
        a = pygame.Vector2(0, 0)
        b = pygame.Vector2(5, 0)
        assert circles_collide(a, 10, b, 10) is True

    def test_touching_circles_not_colliding(self):
        # distance == sum of radii → False (strict less-than)
        a = pygame.Vector2(0, 0)
        b = pygame.Vector2(20, 0)
        assert circles_collide(a, 10, b, 10) is False

    def test_far_apart_circles(self):
        a = pygame.Vector2(0, 0)
        b = pygame.Vector2(100, 0)
        assert circles_collide(a, 10, b, 10) is False

    def test_one_inside_other(self):
        a = pygame.Vector2(0, 0)
        b = pygame.Vector2(1, 0)
        assert circles_collide(a, 50, b, 5) is True

    def test_diagonal_overlap(self):
        a = pygame.Vector2(0, 0)
        b = pygame.Vector2(3, 4)  # distance = 5
        assert circles_collide(a, 3, b, 3) is True  # 3+3=6 > 5

    def test_diagonal_no_overlap(self):
        a = pygame.Vector2(0, 0)
        b = pygame.Vector2(3, 4)  # distance = 5
        assert circles_collide(a, 2, b, 2) is False  # 2+2=4 < 5


# ── rotate_points ─────────────────────────────────────────────
class TestRotatePoints:
    def test_zero_rotation(self):
        points = [(1, 0), (0, 1)]
        result = rotate_points(points, 0)
        assert result[0][0] == pytest.approx(1, abs=1e-9)
        assert result[0][1] == pytest.approx(0, abs=1e-9)

    def test_90_degree_rotation(self):
        points = [(1, 0)]
        result = rotate_points(points, 90)
        # (1,0) rotated 90° → (0, 1)
        assert result[0][0] == pytest.approx(0, abs=1e-9)
        assert result[0][1] == pytest.approx(1, abs=1e-9)

    def test_180_degree_rotation(self):
        points = [(1, 0)]
        result = rotate_points(points, 180)
        assert result[0][0] == pytest.approx(-1, abs=1e-9)
        assert result[0][1] == pytest.approx(0, abs=1e-9)

    def test_negative_angle(self):
        points = [(0, 1)]
        result = rotate_points(points, -90)
        # (0,1) rotated -90° → (1, 0)
        assert result[0][0] == pytest.approx(1, abs=1e-9)
        assert result[0][1] == pytest.approx(0, abs=1e-9)

    def test_multiple_points(self):
        points = [(1, 0), (-1, 0), (0, 1)]
        result = rotate_points(points, 0)
        assert len(result) == 3

    def test_returns_list(self):
        result = rotate_points([(1, 0)], 45)
        assert isinstance(result, list)

    def test_360_returns_original(self):
        points = [(3, 4)]
        result = rotate_points(points, 360)
        assert result[0][0] == pytest.approx(3, abs=1e-9)
        assert result[0][1] == pytest.approx(4, abs=1e-9)
