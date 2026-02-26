---
stepsCompleted:
  - step-01-init
  - step-02-context
  - step-03-starter
  - step-04-decisions
  - step-05-patterns
  - step-06-structure
  - step-07-validation
  - step-08-complete
inputDocuments:
  - '/Users/kousic/Desktop/learn/bmad/_bmad-output/planning-artifacts/prd.md'
  - '/Users/kousic/Desktop/learn/bmad/asteroids-prd.md'
workflowType: 'architecture'
project_name: 'Asteroids (Pygame Clone)'
user_name: 'Kousic'
date: '2026-02-25'
status: 'complete'
completedAt: '2026-02-25'
---

# Architecture Decision Document — Asteroids (Pygame Clone)

**Author:** Kousic
**Date:** 2026-02-25

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

52 FRs across 8 capability areas derived from the PRD:

| Capability Area | FR Count | Architectural Weight |
|---|---|---|
| Ship Control & Physics | FR1–FR9 | High — per-frame kinematics, drag, clamping |
| Game Objects & Behavior | FR10–FR19 | High — procedural polygon gen, edge spawning, wrapping |
| Collision & Scoring | FR20–FR23 | Medium — circle-circle detection across all object pairs |
| Respawn & Invincibility | FR24–FR27 | Medium — safe-zone polling, blink timer |
| Wave & Difficulty Progression | FR28–FR33 | Medium — wave state, speed/interval scaling |
| Game State Management | FR34–FR37 | High — explicit state machine, sub-states |
| Audio | FR38–FR42 | Medium — looping, pitch variants, graceful degradation |
| Visual Rendering & HUD | FR43–FR50 | High — vector polygon rendering, procedural geometry, delta-time |
| Persistence | FR51–FR52 | Low — single JSON read/write with error handling |

**Non-Functional Requirements:**

- **Performance:** 60 FPS enforced via `pygame.Clock.tick(60)` with 30+ simultaneous objects; all physics use delta time
- **Reliability:** Audio and persistence layers must silently degrade on missing/corrupt files — no unhandled exceptions

**Scale & Complexity:**

- Primary domain: Desktop game application
- Complexity level: Medium
- No network, no auth, no database — all complexity is in real-time simulation
- Estimated architectural components: 12 modules + assets directory + test suite

### Technical Constraints & Dependencies

- Language: Python 3.8+ (f-strings, walrus operator safe; no 3.10+ match required)
- Game library: Pygame 2.x (rendering, input, audio, clock)
- Zero additional dependencies — no frameworks, ORMs, or service clients
- All assets bundled locally — no CDN or network fetch
- Single process, single thread — Pygame's event loop is synchronous

### Cross-Cutting Concerns Identified

- **Delta-time physics** — every `update(dt)` call in every game object must use `dt`; inconsistency breaks physics across hardware
- **Screen wrapping** — shared utility used by ship, bullets, asteroids, saucers; must be centralized
- **Graceful audio degradation** — audio load failures must be caught at the sound manager level, not per-call site
- **Object list management** — all game object lists must use copy-on-iterate pattern during removal
- **State machine integrity** — all state transitions must be explicit and exhaustive; no undefined transitions

---

## Starter Template Evaluation

### Primary Technology Domain

Python desktop game application — no conventional web/mobile starter CLI applies. Pygame has no `create-app` equivalent. The project initializes from a `requirements.txt` and a manually structured directory.

### Project Initialization

**No starter CLI available.** The architecture defines the canonical file structure directly.

**Initialization command:**

```bash
mkdir asteroids && cd asteroids
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pygame
pip freeze > requirements.txt
```

### Architectural Decisions Provided by Initialization

| Area | Decision |
|---|---|
| Language | Python 3.8+ |
| Runtime | CPython (standard) |
| Game Library | Pygame 2.x |
| Virtual Environment | venv (stdlib) |
| Dependency Locking | requirements.txt |
| No build tooling | Python runs directly |
| No type checking | Optional mypy post-MVP |
| Testing | pytest (installed separately) |

**Note:** Project initialization and virtual environment setup is the first implementation story.

---

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**

- Game loop pattern: fixed-timestep render loop using `pygame.Clock.tick(60)` returning delta time
- State machine design: explicit enum-based states, centralized in `main.py`
- Physics model: Newtonian kinematics with per-frame drag, all velocity/position in px/s and px/s²
- Object management pattern: Python lists with copy-on-iterate for safe in-loop removal

**Important Decisions (Shape Architecture):**

- Module-per-game-object decomposition (`ship.py`, `asteroid.py`, `bullet.py`, `saucer.py`, `particle.py`)
- All constants isolated in `settings.py` — no magic numbers in game modules
- Audio managed by a dedicated `sounds.py` sound manager class
- High score persistence handled by a dedicated `highscore.py` module

**Deferred Decisions (Post-MVP):**

- Type annotations (mypy) — beneficial but not blocking
- Automated test runner in CI — manual pytest execution sufficient for v1.0
- Multiplayer / network transport — out of scope for v1.0

### Data Architecture

No database. The only persistent data is a single high score value.

- **Storage:** `highscore.json` in the project root directory
- **Format:** `{"high_score": 0}` — single key, integer value
- **Read:** At startup in `highscore.py:load()`
- **Write:** At game over in `highscore.py:save(score)`
- **Error handling:** `FileNotFoundError` → default 0; `json.JSONDecodeError` → default 0 and overwrite

### Authentication & Security

Not applicable — local desktop application with no user accounts, no network, no sensitive data.

### API & Communication Patterns

Not applicable — no external API. Internal communication is direct Python method calls and attribute access within the game loop.

**Internal event pattern:** Pygame's built-in event queue (`pygame.event.get()`) handles OS-level input events only. Game logic events (death, wave clear, score update) are communicated via return values and direct state mutation — no custom event bus.

### Game Loop Architecture

```python
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000.0   # seconds, capped at 60 FPS

    handle_events()    # pygame.event.get() — input + quit
    update(dt)         # physics, collisions, spawning, state transitions
    draw(screen)       # render all objects, HUD, effects
    pygame.display.flip()
```

All game logic runs in `update(dt)`. All rendering runs in `draw(screen)`. These two concerns are never mixed.

### State Machine Architecture

```python
class GameState(Enum):
    TITLE_SCREEN     = auto()
    PLAYING          = auto()
    PAUSED           = auto()
    GAME_OVER        = auto()

# Sub-states (within PLAYING):
class PlaySubState(Enum):
    ACTIVE           = auto()
    RESPAWNING       = auto()
    WAVE_TRANSITION  = auto()
```

State transitions are handled by a single `transition_to(new_state)` method in `main.py`. No state is reachable without an explicit transition call.

### Infrastructure & Deployment

- **Distribution:** Source code only (GitHub) for v1.0
- **Execution:** `python main.py` from project root
- **Dependencies:** `pip install -r requirements.txt`
- **No containerization, no CI/CD, no cloud deployment** — local desktop app

---

## Implementation Patterns & Consistency Rules

### Critical Conflict Points Identified

9 areas where AI agents could make incompatible choices without explicit patterns.

### Naming Patterns

**Python Code Naming (PEP 8 — mandatory):**

| Element | Convention | Example |
|---|---|---|
| Modules / files | `snake_case.py` | `asteroid.py`, `high_score.py` |
| Classes | `PascalCase` | `Asteroid`, `PlayerShip`, `SoundManager` |
| Functions / methods | `snake_case` | `update()`, `draw()`, `check_collision()` |
| Variables | `snake_case` | `asteroid_list`, `player_score` |
| Constants | `UPPER_SNAKE_CASE` in `settings.py` | `MAX_BULLETS`, `ROTATION_SPEED` |
| Boolean flags | `is_` or `has_` prefix | `is_invincible`, `has_thrust` |
| Private attributes | single underscore prefix | `_angle`, `_velocity` |

**Settings Naming:**

All tunable values live in `settings.py`. Names are `UPPER_SNAKE_CASE`. No magic numbers anywhere else in the codebase. Any value referenced in more than one file **must** be a constant in `settings.py`.

### Structure Patterns

**Game Object Interface — all game objects MUST implement:**

```python
class GameObjectName:
    def __init__(self, ...):
        self.pos = pygame.Vector2(x, y)   # position
        self.vel = pygame.Vector2(0, 0)   # velocity in px/s
        self.radius = N                    # collision radius in px
        self.alive = True                  # removal flag

    def update(self, dt: float) -> None:
        """Update physics and state. dt is seconds."""
        ...

    def draw(self, screen: pygame.Surface) -> None:
        """Render to screen."""
        ...
```

Every game object uses `pygame.Vector2` for position and velocity. Never use raw `(x, y)` tuples for physics values.

**Object List Management — copy-on-iterate (mandatory):**

```python
# CORRECT — iterate copy, remove from original
for asteroid in asteroids[:]:
    asteroid.update(dt)
    if not asteroid.alive:
        asteroids.remove(asteroid)

# WRONG — modifying list during iteration
for asteroid in asteroids:
    asteroids.remove(asteroid)   # ❌ NEVER
```

**Screen Wrapping — always via `utils.wrap_position()`:**

```python
# utils.py
def wrap_position(pos: pygame.Vector2, width: int, height: int) -> pygame.Vector2:
    return pygame.Vector2(pos.x % width, pos.y % height)
```

Every `update()` method that moves an object must call `wrap_position()` at the end. Never inline modulo arithmetic.

### Format Patterns

**Delta-Time Physics (mandatory):**

```python
# CORRECT — all movement scaled by dt
self.vel += acceleration * dt
self.pos += self.vel * dt

# WRONG — frame-rate dependent
self.pos.x += 5   # ❌ NEVER without dt
```

**Drag Application:**

```python
# Applied once per frame BEFORE position update
self.vel *= DRAG_COEFFICIENT   # e.g. 0.98 per frame at 60 FPS
```

**Rotation Matrix for Polygon Vertices:**

```python
# utils.py
def rotate_points(points, angle_degrees):
    angle = math.radians(angle_degrees)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a) for x, y in points]
```

All polygon-based objects use this utility. Never implement inline rotation.

**Collision Detection:**

```python
# utils.py
def circles_collide(pos_a, radius_a, pos_b, radius_b) -> bool:
    return pos_a.distance_to(pos_b) < (radius_a + radius_b)
```

All collision checks use this utility. Never inline distance calculations.

### Communication Patterns

**Return values over side effects** — functions that check conditions return booleans or None. State mutations happen in the caller, not deep in utility functions.

**No global mutable state outside `main.py`** — game objects do not reference global score, lives, or state directly. All such values are owned by `main.py` and passed as arguments when needed.

### Process Patterns

**Audio Loading — always guarded:**

```python
# sounds.py — SoundManager.__init__()
try:
    self.fire = pygame.mixer.Sound("assets/sounds/fire.wav")
except (pygame.error, FileNotFoundError):
    self.fire = None

# SoundManager.play(sound)
def play(self, sound):
    if sound is not None:
        sound.play()
```

Never call `pygame.mixer.Sound().play()` directly in game code. Always route through `SoundManager.play()`.

**Persistence Loading — always guarded:**

```python
# highscore.py
def load() -> int:
    try:
        with open(HIGHSCORE_FILE) as f:
            return json.load(f).get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0
```

**Error Handling Philosophy:** Silent degradation for non-critical systems (audio, persistence). No try/except for game logic — let logic bugs surface and crash loudly during development.

### Enforcement Guidelines

**All AI Agents MUST:**

- Use `pygame.Vector2` for all position and velocity values
- Scale all movement by `dt` — no frame-rate-dependent values
- Call `utils.wrap_position()` for screen wrapping — no inline modulo
- Call `utils.circles_collide()` for collision detection — no inline distance math
- Call `utils.rotate_points()` for polygon rotation — no inline trig
- Route all audio through `SoundManager.play()` — no direct `.play()` calls
- Define all tunable values as constants in `settings.py` — no magic numbers
- Use copy-on-iterate (`list[:]`) when removing objects during iteration
- Never mutate global state from inside game object methods

---

## Project Structure & Boundaries

### Complete Project Directory Structure

```
asteroids/
├── main.py              # Game loop, state machine, collision orchestration
├── settings.py          # All constants — screen, physics, gameplay tuning
├── ship.py              # PlayerShip class (FR1–FR9, FR24–FR27, FR44–FR45)
├── asteroid.py          # Asteroid class (FR10–FR12, FR43–FR44)
├── bullet.py            # Bullet class — player + saucer variants (FR18–FR19)
├── saucer.py            # Saucer class, large + small (FR14–FR17)
├── particle.py          # ExplosionParticle class (FR46)
├── hud.py               # HUD rendering (FR48)
├── menu.py              # TitleScreen, GameOverScreen (FR47, FR49–FR50)
├── highscore.py         # High score load/save (FR51–FR52)
├── sounds.py            # SoundManager — load, play, loop (FR38–FR42)
├── utils.py             # wrap_position, circles_collide, rotate_points
├── assets/
│   └── sounds/
│       ├── thrust.wav
│       ├── fire.wav
│       ├── explosion_small.wav
│       ├── explosion_medium.wav
│       ├── explosion_large.wav
│       ├── ship_death.wav
│       ├── saucer_large.wav
│       ├── saucer_small.wav
│       ├── extra_life.wav
│       ├── hyperspace.wav
│       └── beat.wav
├── tests/
│   ├── test_utils.py         # wrap_position, circles_collide, rotate_points
│   ├── test_ship.py          # physics, drag, speed cap, invincibility timer
│   ├── test_asteroid.py      # splitting logic, procedural shape generation
│   ├── test_collision.py     # all 6 collision type combinations
│   ├── test_highscore.py     # load/save, missing file, corrupt file
│   └── test_sounds.py        # SoundManager graceful degradation
├── requirements.txt          # pygame>=2.0.0; pytest for dev
├── README.md
└── highscore.json            # Auto-created at first game over
```

### Architectural Boundaries

**Module Responsibilities:**

| Module | Owns | Does NOT own |
|---|---|---|
| `main.py` | Game loop, state machine, score/lives, wave counter, collision dispatch | Physics calculations, rendering details |
| `settings.py` | All numeric constants and tuning values | Any logic |
| `ship.py` | Ship kinematics, rotation, thrust, invincibility blink timer | Score tracking, wave logic |
| `asteroid.py` | Polygon generation, constant-velocity movement, split logic | Collision outcomes |
| `bullet.py` | Velocity, lifespan countdown | What happens when it hits something |
| `saucer.py` | Movement AI, firing timer, aim calculation | Bullet impact outcomes |
| `particle.py` | Debris scatter and fade animation | Triggering (called by main.py on death) |
| `hud.py` | Rendering score/lives/wave | Score logic |
| `menu.py` | Title and game over screen rendering | State transitions |
| `highscore.py` | File I/O for high score | Game state |
| `sounds.py` | Audio loading and playback routing | Game logic |
| `utils.py` | Pure math utilities | Any game state |

### Requirements to Structure Mapping

**FR1–FR9 (Ship Control & Physics):** `ship.py` + `settings.py` (constants)

**FR10–FR13 (Asteroid Objects):** `asteroid.py`, spawning orchestrated by `main.py`

**FR14–FR17 (Saucer Objects):** `saucer.py`, spawn timer in `main.py`

**FR18–FR19 (Bullets):** `bullet.py`, instantiation by `ship.py` and `saucer.py`

**FR20–FR23 (Collision & Scoring):** `main.py` collision dispatch loop + `utils.circles_collide()`

**FR24–FR27 (Respawn & Invincibility):** `ship.py` (invincibility timer, blink), `main.py` (respawn delay, safe-zone check)

**FR28–FR33 (Wave & Difficulty):** `main.py` (wave state, asteroid count, saucer interval scaling)

**FR34–FR37 (State Machine):** `main.py` (GameState enum, transition_to())

**FR38–FR42 (Audio):** `sounds.py` (SoundManager), triggered from `main.py` and `ship.py`

**FR43–FR50 (Rendering & HUD):** Each object's `draw()` + `hud.py` + `menu.py` + `particle.py`

**FR51–FR52 (Persistence):** `highscore.py`

### Integration Points

**Internal Communication:**

```
main.py
  ├── reads input → updates ship.py (thrust, rotate, fire flags)
  ├── calls update(dt) on all objects each frame
  ├── calls circles_collide() for all object pairs
  ├── on collision → sets alive=False, calls sounds.play(), spawns particles
  ├── checks wave clear condition → triggers WAVE_TRANSITION sub-state
  ├── calls draw(screen) on all objects + hud.draw() + menu.draw()
  └── calls highscore.save() on GAME_OVER transition
```

**Data Flow:**

```
Input Events (keyboard)
    → ship.py (control flags)
    → ship.update(dt) (velocity accumulation)
    → utils.wrap_position() (edge wrapping)
    → main.py collision loop (hit detection)
    → score increment / alive=False
    → particle.py (explosion spawn)
    → sounds.py (sound trigger)
    → hud.py (score display update)
    → highscore.py (save on game over)
```

### File Organization Patterns

**Configuration:** All in `settings.py` — screen dimensions, FPS, physics constants, spawn parameters, scoring values, timing values

**Source Organization:** Flat module layout — no packages/subdirectories for v1.0; 12 modules + utils

**Test Organization:** `tests/` directory, one file per module under test, pytest conventions (`test_*.py`)

**Asset Organization:** `assets/sounds/` — all audio files; no subdirectories needed for v1.0

---

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:** Python 3.8+ and Pygame 2.x are fully compatible. `pygame.Vector2`, `pygame.draw.polygon()`, `pygame.mixer.Sound`, and `pygame.time.Clock` are all stable Pygame 2.x APIs. No dependency conflicts exist.

**Pattern Consistency:** Delta-time physics, `pygame.Vector2`, copy-on-iterate, and centralized utilities are consistent across all game object modules. Naming conventions (PEP 8) are uniformly applicable to all Python modules.

**Structure Alignment:** The flat module structure directly maps to the PRD's §13.1 file structure. Each module has a single clear responsibility. The `utils.py` boundary correctly consolidates shared math operations.

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:** All 52 FRs are traceable to specific modules in the project structure mapping above. No FR is architecturally unsupported.

**Non-Functional Requirements Coverage:**

- Performance (60 FPS, delta-time): `pygame.Clock.tick(60)` in main loop + `dt` param on all `update()` calls ✅
- Performance (30+ objects): flat list iteration in main loop is O(n); acceptable for ≤~80 objects ✅
- Reliability (audio degradation): `SoundManager` guard pattern in `sounds.py` ✅
- Reliability (persistence degradation): try/except in `highscore.load()` ✅
- Reliability (state machine): `GameState` enum + `transition_to()` exhaustive ✅

### Implementation Readiness Validation ✅

**Decision Completeness:** All critical decisions documented with versions. Physics model fully specified (drag coefficient, speed cap, delta-time). State machine design explicit. Object interface contract defined.

**Structure Completeness:** All 12 source modules named with explicit responsibilities. Complete asset directory structure. Test module coverage for all critical subsystems.

**Pattern Completeness:** All 9 potential conflict areas addressed — naming, `Vector2` usage, delta-time, wrapping, collision, rotation, object lists, audio routing, persistence error handling.

### Gap Analysis Results

**No critical gaps identified.**

**Minor gaps (non-blocking):**

- Type annotations not specified — mypy integration deferred to post-MVP
- No linting configuration (flake8/ruff) — optional quality improvement
- No CI/CD pipeline — manual pytest execution sufficient for v1.0
- `beat.wav` heartbeat tempo implementation detail not fully specified — `sounds.py` will manage a looping channel with pitch scaling or channel swap

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed (52 FRs, 3 NFRs, medium complexity)
- [x] Scale and complexity assessed (single-process, single-thread, ~12 modules)
- [x] Technical constraints identified (Python + Pygame only, no deps)
- [x] Cross-cutting concerns mapped (delta-time, wrapping, audio, object lists)

**✅ Architectural Decisions**
- [x] Language and runtime: Python 3.8+ / CPython
- [x] Game library: Pygame 2.x
- [x] Game loop pattern: fixed-timestep with Clock.tick(60)
- [x] State machine: enum-based, centralized in main.py
- [x] Physics model: Newtonian + drag + speed cap + delta-time
- [x] Persistence: highscore.json with graceful error handling
- [x] Audio: SoundManager with graceful degradation

**✅ Implementation Patterns**
- [x] Naming conventions (PEP 8, settings constants)
- [x] Game object interface (Vector2, update/draw, alive flag)
- [x] Object list management (copy-on-iterate)
- [x] Screen wrapping (centralized utility)
- [x] Collision detection (centralized utility)
- [x] Polygon rotation (centralized utility)
- [x] Audio routing (SoundManager.play())
- [x] Persistence error handling (try/except, default 0)

**✅ Project Structure**
- [x] Complete directory tree (12 modules + assets + tests)
- [x] Module responsibility boundaries defined
- [x] FR-to-module mapping complete (all 52 FRs)
- [x] Integration point and data flow documented

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High — all 52 FRs have clear module homes, all cross-cutting concerns have explicit patterns, and the technology stack is simple and well-understood.

**Key Strengths:**

- Zero external dependencies beyond Pygame — no version conflict risk
- Flat module structure matches PRD spec exactly — no translation needed
- Centralized utilities (`utils.py`) prevent pattern drift across agents
- `settings.py` isolation makes the game tunable without touching logic
- Explicit state machine prevents undefined game states

**Areas for Future Enhancement:**

- Add type annotations and mypy for larger team scenarios
- Add `ruff` linting config for code style enforcement
- Consider pytest-cov for coverage tracking post-v1.0

### Implementation Handoff

**AI Agent Guidelines:**

- Follow all architectural decisions exactly as documented
- Use `pygame.Vector2` for all position/velocity — no raw tuples
- Scale all movement by `dt` — no hardcoded pixel increments
- Route audio through `SoundManager.play()` — no direct `.play()` calls
- Define all tunable values in `settings.py` — no magic numbers
- Use copy-on-iterate for all list modifications during iteration
- Refer to this document for all architectural questions

**First Implementation Story:** Project initialization — create virtual environment, install Pygame, verify `python main.py` runs a blank Pygame window with the game loop scaffold.
