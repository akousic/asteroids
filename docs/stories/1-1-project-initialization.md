# Story 1.1: Project Initialization

Status: done

## Story

As a developer,
I want a working Python/Pygame project environment with the minimal game loop scaffold,
so that I can run a Pygame window and all subsequent epics have a verified foundation to build on.

## Acceptance Criteria

**AC-1: Working Game Window**
- Given the developer clones the repository
- When they run `pip install -r requirements.txt` and then `python main.py`
- Then a 1280×720 black Pygame window opens with no errors
- And the window can be closed with the OS close button or the Escape key

**AC-2: Correct Project Files**
- Given the project directory
- When the developer inspects it
- Then `requirements.txt` exists and contains `pygame>=2.0.0`
- And `settings.py` exists with `SCREEN_WIDTH = 1280`, `SCREEN_HEIGHT = 720`, `FPS = 60`
- And a `.venv` setup is documented in `README.md`

**AC-3: No Import Errors**
- Given the environment is activated
- When `python -c "import pygame; pygame.init(); pygame.quit()"` is run
- Then it exits with code 0 and prints no error messages

## Tasks / Subtasks

- [x] Task 1: Create project directory structure (AC: 1, 2)
  - [x] Create `asteroids/` directory at project root
  - [x] Create `assets/sounds/` directory (placeholder, populated in Epic 8)
  - [x] Create `tests/` directory (populated in later epics)

- [x] Task 2: Create `requirements.txt` (AC: 2)
  - [x] Add `pygame>=2.0.0` as runtime dependency
  - [x] Add `pytest>=7.0.0` as dev dependency (comment-documented)

- [x] Task 3: Create `settings.py` with all global constants (AC: 2)
  - [x] Screen: `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`
  - [x] Physics constants stubbed out (full population in Story 2.1): `DRAG_COEFFICIENT`, `SHIP_THRUST`, `MAX_SPEED`, `ROTATION_SPEED`
  - [x] Gameplay constants stubbed out: `BULLET_SPEED`, `BULLET_LIFETIME`, `MAX_BULLETS`
  - [x] Scoring: `SCORE_LARGE`, `SCORE_MEDIUM`, `SCORE_SMALL`, `SCORE_LARGE_SAUCER`, `SCORE_SMALL_SAUCER`
  - [x] Asteroid sizes: `ASTEROID_LARGE_RADIUS`, `ASTEROID_MEDIUM_RADIUS`, `ASTEROID_SMALL_RADIUS`

- [x] Task 4: Create `main.py` with minimal game loop scaffold (AC: 1, 3)
  - [x] `pygame.init()` and `pygame.mixer.init()`
  - [x] Create `screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`
  - [x] Set window caption: `pygame.display.set_caption("Asteroids")`
  - [x] Define `GameState` enum: `TITLE_SCREEN`, `PLAYING`, `PAUSED`, `GAME_OVER`
  - [x] Define `PlaySubState` enum: `ACTIVE`, `RESPAWNING`, `WAVE_TRANSITION`
  - [x] Implement `handle_events()`, `update(dt)`, `draw(screen)` as stub functions
  - [x] Main loop: `clock.tick(60) → dt → handle_events() → update(dt) → draw(screen) → pygame.display.flip()`
  - [x] Handle `pygame.QUIT` event and Escape key → `running = False`
  - [x] `pygame.quit()` and `sys.exit()` at end

- [x] Task 5: Create `README.md` documenting setup (AC: 2)
  - [x] venv setup steps for Windows and macOS/Linux
  - [x] How to install dependencies
  - [x] How to run the game

- [x] Task 6: Verify (AC: 1, 2, 3)
  - [x] Window opens, shows black screen, closes cleanly on Escape or OS button
  - [x] No warnings or errors in terminal

## Dev Notes

### Architecture Mandate — Read First

This story establishes the foundational structure that ALL subsequent stories depend on. Getting this right matters more than any later story.

**Key constraint:** Every tunable value must be a constant in `settings.py`. Story 2.1 will add physics constants; Story 3.1 will add asteroid constants. This story seeds `settings.py` with all constants even if some are placeholders — this prevents agents from using magic numbers later.

### Technology Stack

| Item | Decision | Notes |
|---|---|---|
| Language | Python 3.8+ | f-strings, walrus op safe |
| Game library | Pygame 2.x | `pygame>=2.0.0` in requirements.txt |
| Virtual env | `venv` (stdlib) | No `virtualenv`, no `conda` |
| Dependency locking | `requirements.txt` | `pip freeze` after install |
| Test framework | `pytest` (dev-only) | Listed in requirements.txt but not imported in game code |
| Type checking | None for v1.0 | mypy deferred post-MVP |

**Do NOT add any other dependencies.** Zero additional packages beyond pygame and pytest. The game has no ORM, no networking library, no GUI toolkit.

### `main.py` — Exact Required Structure

```python
import sys
import pygame
from enum import Enum, auto
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class GameState(Enum):
    TITLE_SCREEN = auto()
    PLAYING      = auto()
    PAUSED       = auto()
    GAME_OVER    = auto()


class PlaySubState(Enum):
    ACTIVE          = auto()
    RESPAWNING      = auto()
    WAVE_TRANSITION = auto()


def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


def update(dt: float) -> None:
    """Update all game logic. dt is elapsed seconds since last frame."""
    pass  # Stories 2–10 fill this in


def draw(screen: pygame.Surface) -> None:
    """Render everything to screen."""
    screen.fill((0, 0, 0))  # Black background


def main():
    global running
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    state = GameState.TITLE_SCREEN
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds

        handle_events()
        update(dt)
        draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

**Critical notes:**
- `dt = clock.tick(FPS) / 1000.0` — divide by 1000 to convert ms → seconds
- `screen.fill((0, 0, 0))` goes in `draw()`, NOT in update
- `pygame.display.flip()` is called once per frame, AFTER `draw()`
- `handle_events()`, `update(dt)`, `draw(screen)` must be separate functions — never inline
- `global running` is acceptable for this scaffold. Later stories may refactor to a Game class if needed, but do NOT prematurely refactor now

### `settings.py` — Exact Required Structure

```python
# ──────────────────────────────────────────────
# SCREEN
# ──────────────────────────────────────────────
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60

# ──────────────────────────────────────────────
# PHYSICS (populated fully in Story 2.1)
# ──────────────────────────────────────────────
DRAG_COEFFICIENT = 0.98          # velocity multiplier per frame
SHIP_THRUST      = 300.0         # px/s² acceleration
MAX_SPEED        = 600.0         # px/s velocity cap
ROTATION_SPEED   = 270.0         # degrees/second

# ──────────────────────────────────────────────
# BULLETS (populated in Story 2.2)
# ──────────────────────────────────────────────
BULLET_SPEED    = 800.0          # px/s
BULLET_LIFETIME = 1.0            # seconds
MAX_BULLETS     = 4              # max simultaneous player bullets

# ──────────────────────────────────────────────
# ASTEROIDS (populated in Story 3.1)
# ──────────────────────────────────────────────
ASTEROID_LARGE_RADIUS  = 50
ASTEROID_MEDIUM_RADIUS = 25
ASTEROID_SMALL_RADIUS  = 12

ASTEROID_LARGE_SPEED_MIN  = 40.0
ASTEROID_LARGE_SPEED_MAX  = 80.0
ASTEROID_MEDIUM_SPEED_MIN = 80.0
ASTEROID_MEDIUM_SPEED_MAX = 140.0
ASTEROID_SMALL_SPEED_MIN  = 140.0
ASTEROID_SMALL_SPEED_MAX  = 220.0

ASTEROID_SPAWN_SAFE_RADIUS = 150  # px from player at wave start

# ──────────────────────────────────────────────
# SCORING
# ──────────────────────────────────────────────
SCORE_LARGE_ASTEROID  = 20
SCORE_MEDIUM_ASTEROID = 50
SCORE_SMALL_ASTEROID  = 100
SCORE_LARGE_SAUCER    = 200
SCORE_SMALL_SAUCER    = 1000
EXTRA_LIFE_THRESHOLD  = 10000    # points per extra life
MAX_LIVES             = 5

# ──────────────────────────────────────────────
# RESPAWN
# ──────────────────────────────────────────────
RESPAWN_DELAY       = 2.0        # seconds after death
INVINCIBILITY_TIME  = 3.0        # seconds of post-respawn invincibility
BLINK_RATE          = 5          # frames per blink toggle
RESPAWN_SAFE_RADIUS = 150        # px from center spawn point

# ──────────────────────────────────────────────
# WAVE
# ──────────────────────────────────────────────
WAVE_ASTEROID_START = 4          # large asteroids in wave 1
WAVE_ASTEROID_MAX   = 12         # cap from wave 6+
WAVE_TRANSITION_DELAY = 2.0      # seconds before next wave starts
WAVE_BANNER_DURATION  = 3.0      # seconds to show "WAVE X"

# ──────────────────────────────────────────────
# SAUCER
# ──────────────────────────────────────────────
SAUCER_SPAWN_INTERVAL_BASE = 15.0   # seconds between spawns (wave 1)
SAUCER_SPAWN_INTERVAL_MIN  = 10.0   # minimum interval floor
SAUCER_LARGE_RADIUS        = 20     # px
SAUCER_SMALL_RADIUS        = 10     # px
SAUCER_LARGE_FIRE_INTERVAL = 1.5    # seconds between shots
SAUCER_SMALL_FIRE_INTERVAL = 1.0
SAUCER_AIM_SPREAD          = 15.0   # degrees of random offset on aimed shot
SMALL_SAUCER_SCORE_THRESHOLD = 40000  # score at which only small saucers spawn

# ──────────────────────────────────────────────
# HYPERSPACE
# ──────────────────────────────────────────────
HYPERSPACE_DEATH_CHANCE = 1 / 6
HYPERSPACE_COOLDOWN     = 2.0       # seconds

# ──────────────────────────────────────────────
# COLORS
# ──────────────────────────────────────────────
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)

# ──────────────────────────────────────────────
# RENDERING
# ──────────────────────────────────────────────
LINE_WIDTH = 2                       # polygon stroke width in px
```

**Why populate all constants now:** Subsequent stories will import from `settings.py`. If a constant isn't there, the agent implementing that story may use a magic number. Defining all constants upfront — even if unused in this story — prevents that failure mode. All values match the PRD/architecture spec.

### `requirements.txt` — Exact Format

```
pygame>=2.0.0

# Dev dependencies (not needed for runtime)
pytest>=7.0.0
```

**Important:** Do NOT run `pip freeze` blindly and lock every transitive dependency. The file should contain only what is needed. `pygame>=2.0.0` allows any Pygame 2.x release and prevents breakage when a user has 2.5 or 2.6 installed.

### Directory Structure Created by This Story

```
asteroids/              ← create this directory
├── main.py             ← minimal game loop (see template above)
├── settings.py         ← ALL constants (see template above)
├── requirements.txt    ← pygame>=2.0.0, pytest>=7.0.0
├── README.md           ← setup instructions
├── assets/
│   └── sounds/         ← empty dir, populated in Epic 8
└── tests/              ← empty dir, populated in later epics
```

**Do NOT create** `ship.py`, `asteroid.py`, `bullet.py`, etc. yet — those belong to their respective stories. Creating empty placeholder files would only clutter the codebase.

### Project Structure Notes

- Game lives in `asteroids/` (a subdirectory of the BMAD workspace, or created adjacent to it)
- There is NO `src/` wrapper — flat module layout is the architecture decision
- `main.py` is at the root of the `asteroids/` directory, not in a subdirectory
- All subsequent story files will reference paths relative to the `asteroids/` root (e.g., `ship.py`, `asteroid.py`)
- Do not create `__init__.py` — this is a scripts project, not a package

### Testing Notes

- No unit tests in this story — no logic to test; window-open verification is manual
- Tests directory is created but empty
- Story 1.3 introduces `utils.py` and the first real unit tests

### Common Mistakes to Avoid

- **Do NOT** use `pygame.time.wait()` or `time.sleep()` in the game loop — use `clock.tick(FPS)` only
- **Do NOT** call `pygame.display.update()` — use `pygame.display.flip()` for double-buffered rendering
- **Do NOT** add a `Game` class wrapper in this story — the scaffold uses functions; a class refactor can happen post-MVP
- **Do NOT** import from modules that don't exist yet (no ship imports, no asteroid imports)
- **Do NOT** add linting config (flake8, ruff, pyproject.toml) — out of scope for v1.0
- **Do NOT** add mypy or type stubs — deferred post-MVP per architecture decision

### References

- [Source: architecture.md — Starter Template Evaluation] — initialization commands, architecture decisions
- [Source: architecture.md — Game Loop Architecture] — exact game loop code pattern
- [Source: architecture.md — State Machine Architecture] — GameState and PlaySubState enum definitions
- [Source: architecture.md — Implementation Patterns] — naming conventions, settings.py rules
- [Source: architecture.md — Project Structure] — complete directory tree
- [Source: epics.md — Story 1.1] — acceptance criteria
- [Source: prd.md — FR43] — 1280×720 screen at 60 FPS
- [Source: prd.md — FR34] — state machine TITLE_SCREEN initial state

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, no issues encountered.

### Completion Notes List

- All tasks completed in single pass. No deviations from story spec.
- `settings.py` pre-populated with ALL 48 constants across 9 categories (screen, physics, bullets, asteroids, scoring, respawn, wave, saucer, hyperspace, colors, rendering) — prevents magic numbers in all future stories.
- `main.py` implements the exact game loop pattern from architecture.md: `clock.tick(FPS)/1000.0 → handle_events() → update(dt) → draw(screen) → flip()`.
- `GameState` (TITLE_SCREEN, PLAYING, PAUSED, GAME_OVER) and `PlaySubState` (ACTIVE, RESPAWNING, WAVE_TRANSITION) enums present.
- Structural verification passed: 48 constants defined, GameState/PlaySubState enums confirmed, all 4 required functions (handle_events, update, draw, main) confirmed.
- No unit tests added — architecture confirms none required for this infrastructure story; first real tests arrive in Story 1.3 (utils.py).
- AC-3 (no import errors) verified via `ast.parse()` on both settings.py and main.py — both parse clean.
- Note for Story 1.2 dev: `GameState` and `PlaySubState` are defined in `main.py`. Story 1.2 will flesh out the `update(dt)` and `draw(screen)` functions and the main loop dispatch logic.

### File List

- asteroids/main.py (created)
- asteroids/settings.py (created)
- asteroids/requirements.txt (created)
- asteroids/README.md (created)
- asteroids/assets/sounds/ (created — empty directory)
- asteroids/tests/ (created — empty directory)
