import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class TitleScreen:
    """Animated title screen with pulsing text."""

    def __init__(self, font: pygame.font.Font) -> None:
        self._font = font
        self._small = pygame.font.SysFont(None, 32)
        self._pulse = 0.0
        self._blink_timer = 0.0
        self._show_prompt = True

    def update(self, dt: float) -> None:
        self._pulse += dt * 2.0
        self._blink_timer += dt
        if self._blink_timer >= 0.6:
            self._blink_timer = 0.0
            self._show_prompt = not self._show_prompt

    def draw(self, screen: pygame.Surface) -> None:
        import math
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2

        # Title
        title_surf = self._font.render("ASTEROIDS", True, WHITE)
        title_rect = title_surf.get_rect(center=(cx, cy - 80))
        screen.blit(title_surf, title_rect)

        # Subtitle
        sub = self._small.render("A PYGAME CLONE", True, WHITE)
        sub_rect = sub.get_rect(center=(cx, cy - 40))
        screen.blit(sub, sub_rect)

        # Prompt (blinking)
        if self._show_prompt:
            prompt = self._small.render("PRESS ENTER OR SPACE TO START", True, WHITE)
            prompt_rect = prompt.get_rect(center=(cx, cy + 20))
            screen.blit(prompt, prompt_rect)

        # Controls
        controls = [
            "W / UP    - Thrust",
            "A/D / LEFT/RIGHT - Rotate",
            "SPACE     - Fire",
            "SHIFT     - Hyperspace",
            "P / ESC   - Pause",
        ]
        ctrl_font = pygame.font.SysFont(None, 26)
        for i, line in enumerate(controls):
            surf = ctrl_font.render(line, True, (180, 180, 180))
            rect = surf.get_rect(center=(cx, cy + 80 + i * 24))
            screen.blit(surf, rect)


class GameOverScreen:
    """Game over screen showing final score and high score."""

    def __init__(self, font: pygame.font.Font, score: int, high_score: int) -> None:
        self._font = font
        self._small = pygame.font.SysFont(None, 36)
        self._score = score
        self._high_score = high_score
        self._new_record = score >= high_score and score > 0
        self._blink_timer = 0.0
        self._show_prompt = True

    def update(self, dt: float) -> None:
        self._blink_timer += dt
        if self._blink_timer >= 0.6:
            self._blink_timer = 0.0
            self._show_prompt = not self._show_prompt

    def draw(self, screen: pygame.Surface) -> None:
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2

        # Game Over
        go_surf = self._font.render("GAME OVER", True, WHITE)
        go_rect = go_surf.get_rect(center=(cx, cy - 80))
        screen.blit(go_surf, go_rect)

        # Score
        score_surf = self._small.render(f"SCORE: {self._score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(cx, cy - 30))
        screen.blit(score_surf, score_rect)

        # High score
        hs_surf = self._small.render(f"HIGH SCORE: {self._high_score}", True, WHITE)
        hs_rect = hs_surf.get_rect(center=(cx, cy + 10))
        screen.blit(hs_surf, hs_rect)

        # New record
        if self._new_record:
            nr_surf = self._small.render("NEW HIGH SCORE!", True, WHITE)
            nr_rect = nr_surf.get_rect(center=(cx, cy + 50))
            screen.blit(nr_surf, nr_rect)

        # Prompt (blinking)
        if self._show_prompt:
            tiny = pygame.font.SysFont(None, 30)
            p = tiny.render("PRESS ENTER, SPACE, OR ESC", True, WHITE)
            p_rect = p.get_rect(center=(cx, cy + 95))
            screen.blit(p, p_rect)
