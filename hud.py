import math
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, LINE_WIDTH, MAX_LIVES
from utils import rotate_points


# Mini ship silhouette for life indicators (scaled down)
_MINI_SHIP = [
    (0, -8),
    (5, 4),
    (0, 2),
    (-5, 4),
]


def _draw_mini_ship(screen: pygame.Surface, cx: float, cy: float) -> None:
    """Draw a small ship icon at (cx, cy)."""
    world_pts = [(cx + x, cy + y) for x, y in _MINI_SHIP]
    pygame.draw.polygon(screen, WHITE, world_pts, 1)


class HUD:
    """Renders the in-game HUD: score, high score, wave number, life indicators."""

    def __init__(self, font: pygame.font.Font) -> None:
        self._font = font
        self._small_font = pygame.font.SysFont(None, 32)

    def draw(
        self,
        screen: pygame.Surface,
        score: int,
        lives: int,
        wave: int,
        high_score: int,
    ) -> None:
        # Score — top left
        score_surf = self._font.render(str(score), True, WHITE)
        screen.blit(score_surf, (20, 15))

        # High score — top center
        hs_surf = self._small_font.render(f"HI {high_score}", True, WHITE)
        hs_rect = hs_surf.get_rect(midtop=(SCREEN_WIDTH // 2, 18))
        screen.blit(hs_surf, hs_rect)

        # Wave number — top right
        wave_surf = self._small_font.render(f"WAVE {wave}", True, WHITE)
        wave_rect = wave_surf.get_rect(topright=(SCREEN_WIDTH - 20, 18))
        screen.blit(wave_surf, wave_rect)

        # Life indicators — row of mini ships below score
        for i in range(min(lives, MAX_LIVES)):
            _draw_mini_ship(screen, 28 + i * 22, 60)
