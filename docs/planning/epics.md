---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
status: complete
completedAt: '2026-02-25'
inputDocuments:
  - '/Users/kousic/Desktop/learn/bmad/_bmad-output/planning-artifacts/prd.md'
  - '/Users/kousic/Desktop/learn/bmad/_bmad-output/planning-artifacts/architecture.md'
---

# Asteroids (Pygame Clone) - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Asteroids (Pygame Clone), decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Player can rotate the ship left/right continuously while keys are held (270°/second)
FR2: Player can apply thrust in the ship's facing direction, accumulating velocity
FR3: Ship velocity decays by drag coefficient ×0.98 per frame when thrust is not applied
FR4: Ship velocity is clamped to a maximum of 600 px/s
FR5: Player can fire one bullet per key press in the ship's facing direction (Space key)
FR6: Player can activate hyperspace to teleport the ship to a random screen position
FR7: Hyperspace carries a 1-in-6 probability of destroying the ship on re-entry
FR8: Hyperspace has a 2-second cooldown between activations
FR9: Player can pause and unpause the game (Esc or P)
FR10: Asteroids spawn at random screen edge positions at wave start, at least 150 px from the player
FR11: Large and medium asteroids split into 2 smaller asteroids on destruction; small asteroids are destroyed outright
FR12: Child asteroids inherit parent position and travel at parent angle ±20–60° random offset
FR13: All game objects (ship, bullets, asteroids, saucers) wrap around all four screen edges
FR14: Large saucer spawns on a timed interval, moves horizontally with random vertical direction changes every 1–2 seconds, fires randomly every 1.5 seconds
FR15: Small saucer spawns after player reaches 40,000 points, fires aimed shots toward player with ±15° random offset every 1.0 second
FR16: At most one saucer is on screen at any time
FR17: Saucer bullets can destroy asteroids and the player ship
FR18: Player bullets are destroyed on contact with asteroids or saucers; max 4 player bullets on screen simultaneously
FR19: Player bullets despawn after 1.0 seconds regardless of contact
FR20: Player earns points when a bullet destroys an asteroid (large: 20 / medium: 50 / small: 100)
FR21: Player earns points when a bullet destroys a saucer (large: 200 / small: 1,000)
FR22: Player loses a life when the ship collides with an asteroid, saucer, or saucer bullet
FR23: Player earns one extra life at every 10,000 points; lives are capped at 5
FR24: Ship respawns at screen center after a 2-second delay following death
FR25: Respawn is delayed while any asteroid is within 150 px of the center spawn point
FR26: Ship has 3 seconds of collision invincibility after respawning; ship blinks (toggle every 5 frames) to signal this state
FR27: Player can fire during the invincibility period
FR28: Each wave begins with a set count of large asteroids (wave 1: 4, +1/wave, capped at 12 from wave 6+)
FR29: Next wave begins after a 2-second pause once all asteroids are destroyed and no saucer is active
FR30: "WAVE X" is displayed in the top-right for 3 seconds at wave start
FR31: Saucer spawn interval decreases by 1 second per wave (minimum 10 seconds)
FR32: Asteroid speed range increases ~5% per wave after wave 5
FR33: Only small saucers spawn once the player exceeds 40,000 points
FR34: Game transitions correctly through all states: TITLE_SCREEN → PLAYING → PAUSED → GAME_OVER → TITLE_SCREEN
FR35: Sub-states RESPAWNING and WAVE_TRANSITION operate within PLAYING without breaking outer state flow
FR36: Game over screen returns to title on Enter key press or after a 10-second auto-timeout
FR37: Game over triggers when the player loses their last life
FR38: Thrust sound loops while the thrust key is held and stops when released
FR39: Distinct sound effects play for: bullet fire, asteroid explosion (per size), ship death, saucer destruction, extra life awarded, hyperspace activation
FR40: Saucer alarm loops while a saucer is on screen; large and small saucers use different pitches
FR41: Background heartbeat tempo scales from ~1 beat/second (many asteroids) to ~4 beats/second (few asteroids remaining)
FR42: Missing audio files do not crash the game; audio events are silently skipped
FR43: All game objects render as white vector-line polygons (2 px line width) on a black background at 60 FPS
FR44: Each asteroid instance is a procedurally generated irregular polygon (8–12 vertices, radii ±30% of base radius)
FR45: Thrust flame renders as a flickering triangle at the ship's rear when thrusting (toggles every 3–4 frames)
FR46: Explosion animations render as line-segment debris that scatter outward and fade (asteroids: 0.5 s, ship: 1.0 s, saucer: 0.5 s)
FR47: Objects near screen edges render at both the current and wrapped opposite position to prevent visual pop
FR48: HUD displays: current score (top-left, ~28px), high score (top-center, ~22px), ship-icon lives (top-left below score), wave number (top-right, 3 s at wave start)
FR49: Title screen shows game title, flashing "PRESS ENTER TO START", current high score, and non-interactive drifting asteroids
FR50: Game over screen shows final score and "NEW HIGH SCORE!" when applicable
FR51: High score is written to `highscore.json` at game over
FR52: High score is read from `highscore.json` at startup; missing or corrupt file defaults to 0 without crashing

### NonFunctional Requirements

NFR1: The game shall maintain 60 FPS as enforced by `pygame.Clock.tick(60)` with 30+ simultaneous active objects on screen
NFR2: All physics and movement calculations shall use delta time (dt in seconds) to ensure frame-rate-independent behavior across hardware
NFR3: Collision detection shall complete within a single frame budget (≤16.6 ms) for all active object pairs in a worst-case wave scenario
NFR4: Audio manager shall catch `pygame.error` and `FileNotFoundError` on sound load and continue silently — no missing sound file may raise an unhandled exception
NFR5: Persistence layer shall catch `FileNotFoundError`, `json.JSONDecodeError`, and `PermissionError` on `highscore.json` read/write, defaulting to score 0 and continuing without interruption
NFR6: All game state transitions shall be explicitly enumerated — no game state shall be reachable without a defined transition path

### Additional Requirements

- Project initialization: create virtual environment (`python -m venv .venv`), install Pygame 2.x, verify blank Pygame window runs — this is Story 1.1
- All 12 source modules must be created: `main.py`, `settings.py`, `ship.py`, `asteroid.py`, `bullet.py`, `saucer.py`, `particle.py`, `hud.py`, `menu.py`, `highscore.py`, `sounds.py`, `utils.py`
- All tunable values must be defined as constants in `settings.py` — no magic numbers in game modules
- `utils.py` must provide three centralized utilities: `wrap_position()`, `circles_collide()`, `rotate_points()`
- All game object classes must implement the `update(dt)` / `draw(screen)` interface with `pygame.Vector2` for position/velocity
- Copy-on-iterate pattern (`list[:]`) required whenever objects are removed during iteration
- `SoundManager` class in `sounds.py` must guard all audio loads with try/except and route all playback through `SoundManager.play()`
- `highscore.py` must guard all file I/O with try/except covering `FileNotFoundError`, `json.JSONDecodeError`, `PermissionError`
- `requirements.txt` must pin `pygame>=2.0.0`; pytest listed as dev dependency

### FR Coverage Map

| Story | FRs Covered |
|---|---|
| 1.1 Project Setup | — (infrastructure) |
| 1.2 Core Scaffold | NFR1, NFR2, NFR6, FR34 (partial) |
| 1.3 Shared Utilities | FR13, FR47 (wrap), collision geometry, rotation geometry |
| 2.1 Ship Rendering & Physics | FR1, FR2, FR3, FR4, FR43, FR45, NFR2 |
| 2.2 Player Bullets | FR5, FR18, FR19, FR43 |
| 2.3 Ship Wrapping | FR13 (ship + bullet) |
| 3.1 Asteroid Spawning & Shape | FR10, FR44 |
| 3.2 Asteroid Movement & Wrapping | FR13 (asteroids), NFR2 |
| 3.3 Asteroid Splitting | FR11, FR12 |
| 4.1 Collision Detection Framework | FR20, FR21, FR22, NFR3 |
| 4.2 Bullet–Asteroid Collisions | FR20 |
| 4.3 Ship–Asteroid Collisions | FR22 |
| 5.1 Score & Lives System | FR20, FR21, FR22, FR23 |
| 5.2 Respawn System | FR24, FR25, FR26, FR27 |
| 5.3 Wave Progression | FR28, FR29, FR30 |
| 6.1 State Machine | FR34, FR35, FR36, FR37, NFR6 |
| 6.2 Pause System | FR9, FR34 |
| 6.3 HUD | FR48 |
| 6.4 Title & Game Over Screens | FR49, FR50, FR36 |
| 7.1 High Score Persistence | FR51, FR52, NFR5 |
| 7.2 Large Saucer | FR14, FR16 |
| 7.3 Small Saucer & Difficulty Scaling | FR15, FR16, FR31, FR32, FR33 |
| 7.4 Saucer Bullets & Collisions | FR17, FR21 |
| 7.5 Hyperspace | FR6, FR7, FR8 |
| 8.1 Sound Manager & Basic SFX | FR38, FR39, FR42, NFR4 |
| 8.2 Saucer Alarm & Heartbeat | FR40, FR41 |
| 9.1 Explosion Particles | FR46 |
| 9.2 Edge-Wrapping Visual Fix | FR47 |
| 9.3 Extra Life Visual & SFX | FR23, FR39 (extra life sound) |
| 10.1 Full Integration & Acceptance Testing | All 52 FRs + 6 NFRs |

## Epic List

1. **Epic 1: Project Foundation** — Environment, scaffold, shared utilities
2. **Epic 2: Player Ship** — Ship rendering, physics, bullets
3. **Epic 3: Asteroids** — Spawning, movement, splitting
4. **Epic 4: Collision Detection** — All collision pairs
5. **Epic 5: Game Loop Core** — Score, lives, respawn, wave progression
6. **Epic 6: Game States & UI** — State machine, pause, HUD, menus
7. **Epic 7: Advanced Gameplay** — High score, saucers, hyperspace
8. **Epic 8: Audio** — Sound manager, SFX, heartbeat
9. **Epic 9: Visual Polish** — Particles, edge rendering, extra life indicators
10. **Epic 10: Integration & Acceptance** — Full integration testing against all 52 FRs

---

## Epic 1: Project Foundation

**Goal:** Establish the working Python/Pygame development environment, the game loop scaffold, and shared utility functions that all subsequent epics depend on.

### Story 1.1: Project Initialization

As a developer,
I want a working Python/Pygame project environment,
So that I can run a Pygame window and begin building the game.

**Acceptance Criteria:**

**Given** the developer clones the repository
**When** they run `pip install -r requirements.txt` and then `python main.py`
**Then** a 1280×720 black Pygame window opens with no errors
**And** the window can be closed with the OS close button or Escape

**Given** the project directory
**When** the developer inspects it
**Then** `requirements.txt` exists and pins `pygame>=2.0.0`
**And** `settings.py` exists with `SCREEN_WIDTH = 1280`, `SCREEN_HEIGHT = 720`, `FPS = 60`
**And** a `.venv` setup is documented in `README.md`

---

### Story 1.2: Game Loop Scaffold

As a developer,
I want the core game loop with delta time and state machine stub,
So that all subsequent modules have a consistent update/draw cycle to plug into.

**Acceptance Criteria:**

**Given** the game is running
**When** each frame executes
**Then** `dt = clock.tick(60) / 1000.0` produces a float in seconds
**And** `handle_events()`, `update(dt)`, and `draw(screen)` are called in that order
**And** `pygame.display.flip()` is called once per frame

**Given** the `GameState` enum is defined
**When** the game starts
**Then** initial state is `GameState.TITLE_SCREEN`
**And** `GameState` contains: `TITLE_SCREEN`, `PLAYING`, `PAUSED`, `GAME_OVER`
**And** `PlaySubState` contains: `ACTIVE`, `RESPAWNING`, `WAVE_TRANSITION`

---

### Story 1.3: Shared Utilities

As a developer,
I want centralized utility functions for wrapping, collision, and rotation,
So that all game objects use consistent math with no duplicated logic.

**Acceptance Criteria:**

**Given** `utils.py` exists
**When** `wrap_position(pos, width, height)` is called with a `pygame.Vector2` outside screen bounds
**Then** it returns a `pygame.Vector2` with coordinates wrapped via modulo
**And** `wrap_position(Vector2(1290, 50), 1280, 720)` returns `Vector2(10.0, 50.0)`

**Given** `utils.circles_collide(pos_a, r_a, pos_b, r_b)` is called
**When** distance between centers is less than sum of radii
**Then** it returns `True`
**When** distance is greater than or equal to sum of radii
**Then** it returns `False`

**Given** `utils.rotate_points(points, angle_degrees)` is called
**When** a list of `(x, y)` tuples and an angle are provided
**Then** it returns a new list of rotated tuples using a 2D rotation matrix
**And** rotating by 0 degrees returns the original points unchanged

---

## Epic 2: Player Ship

**Goal:** Implement the player ship with full Newtonian physics, keyboard controls, bullet firing, and screen wrapping.

### Story 2.1: Ship Rendering and Physics

As a player,
I want my ship to thrust, rotate, and drift with realistic Newtonian physics,
So that movement feels authentic to the original Asteroids.

**Acceptance Criteria:**

**Given** the game is in `PLAYING` state
**When** the player holds W (or Up Arrow)
**Then** the ship accelerates in its current facing direction at 300 px/s²
**And** a flickering thrust flame triangle renders at the ship's rear (toggles every 3–4 frames)

**Given** the player releases the thrust key
**When** the next frame updates
**Then** velocity decays by `×0.98` per frame (drag)
**And** the ship continues drifting without stopping instantly

**Given** the player holds A or D
**When** the next frame updates
**Then** the ship rotates at 270°/second in the corresponding direction

**Given** the ship's velocity exceeds 600 px/s
**When** the frame updates
**Then** velocity magnitude is clamped to 600 px/s

**Given** the ship is rendered
**When** drawn to screen
**Then** it appears as a white isosceles triangle outline (3-vertex polygon, 2 px line width, ~40 px tall × ~24 px wide)
**And** all physics calculations use `dt` (seconds)

---

### Story 2.2: Player Bullets

As a player,
I want to fire bullets in my ship's facing direction,
So that I can destroy asteroids.

**Acceptance Criteria:**

**Given** the game is in `PLAYING / ACTIVE` sub-state
**When** the player presses Space
**Then** one bullet is created at the ship's nose, traveling at 800 px/s in the ship's facing direction
**And** the bullet is added to the bullet list

**Given** 4 bullets are already on screen
**When** the player presses Space
**Then** no new bullet is created (max 4 enforced)

**Given** a bullet has been alive for 1.0 seconds
**When** the frame updates
**Then** the bullet is removed from the bullet list (`alive = False`)

**Given** a bullet is rendered
**When** drawn to screen
**Then** it appears as a small white circle or 2×2 px square

---

### Story 2.3: Ship and Bullet Screen Wrapping

As a player,
I want my ship and bullets to wrap around screen edges seamlessly,
So that no object is lost off-screen.

**Acceptance Criteria:**

**Given** the ship moves past the right screen edge
**When** the position updates
**Then** the ship reappears at the left edge at the same vertical position
**And** the same behavior applies to all four edges

**Given** a bullet moves past any screen edge
**When** the position updates
**Then** it wraps to the opposite edge

**Given** an object is within one radius of a screen edge
**When** it is drawn
**Then** it is drawn at both its current position and the wrapped opposite position (prevents visual pop)

---

## Epic 3: Asteroids

**Goal:** Implement asteroid spawning, procedural polygon generation, movement, screen wrapping, and splitting behavior.

### Story 3.1: Asteroid Spawning and Shape Generation

As a player,
I want asteroids that look unique and spawn at wave start,
So that each wave feels visually distinct.

**Acceptance Criteria:**

**Given** a new wave begins
**When** asteroids are spawned
**Then** they appear at random positions along the screen edges
**And** no asteroid spawns within 150 px of the player's position

**Given** an asteroid is created
**When** its polygon is generated
**Then** it has 8–12 vertices at evenly spaced angles
**And** each vertex radius is `base_radius × random.uniform(0.7, 1.3)`
**And** base radii are: large = 50 px, medium = 25 px, small = 12 px

**Given** two asteroids of the same size are created in the same session
**When** they are drawn
**Then** their polygon shapes are visually different (procedural uniqueness)

---

### Story 3.2: Asteroid Movement and Wrapping

As a player,
I want asteroids to move in straight lines at constant speed and wrap the screen,
So that they behave consistently with the original game.

**Acceptance Criteria:**

**Given** an asteroid is spawned
**When** it moves each frame
**Then** it travels in a straight line at constant speed (no acceleration, no drag)
**And** speed is within range: large 40–80 px/s, medium 80–140 px/s, small 140–220 px/s
**And** all movement uses `dt`

**Given** an asteroid reaches any screen edge
**When** the position updates
**Then** it wraps to the opposite edge (same logic as `utils.wrap_position()`)

---

### Story 3.3: Asteroid Splitting

As a player,
I want destroyed asteroids to split into smaller ones,
So that the asteroid field grows more chaotic as I shoot.

**Acceptance Criteria:**

**Given** a player bullet hits a large asteroid
**When** the collision is resolved
**Then** the large asteroid is destroyed (`alive = False`)
**And** 2 medium asteroids spawn at the large asteroid's position
**And** each child travels at a diverging angle (parent angle ±20–60° random offset)

**Given** a player bullet hits a medium asteroid
**When** the collision is resolved
**Then** 2 small asteroids spawn using the same divergence logic

**Given** a player bullet hits a small asteroid
**When** the collision is resolved
**Then** the asteroid is destroyed with no children spawned

---

## Epic 4: Collision Detection

**Goal:** Implement the collision detection framework and handle all 6 collision pair types correctly.

### Story 4.1: Collision Detection Framework

As a developer,
I want a centralized collision dispatch loop in `main.py`,
So that all collision types are checked consistently using circle-circle detection.

**Acceptance Criteria:**

**Given** any two game objects with `pos`, `radius`, and `alive` attributes
**When** `utils.circles_collide()` is called with their positions and radii
**Then** it correctly returns `True` when overlapping and `False` when not

**Given** the collision loop runs each frame
**When** it checks all object pairs
**Then** it only checks pairs where both objects have `alive = True`
**And** it completes within 16.6 ms for worst-case wave scenarios (NFR3)

---

### Story 4.2: Bullet–Object Collisions

As a player,
I want my bullets to destroy asteroids and saucers on contact,
So that I can clear the field and earn points.

**Acceptance Criteria:**

**Given** a player bullet overlaps an asteroid (any size)
**When** the collision is detected
**Then** the bullet's `alive` is set to `False`
**And** the asteroid's splitting/destruction logic is triggered
**And** correct points are awarded (FR20)

**Given** a player bullet overlaps a saucer
**When** the collision is detected
**Then** the bullet and saucer are both set to `alive = False`
**And** correct points are awarded (FR21)

**Given** a saucer bullet overlaps an asteroid
**When** the collision is detected
**Then** the saucer bullet is destroyed and the asteroid splits/destroys
**And** no points are awarded to the player

---

### Story 4.3: Ship–Threat Collisions

As a player,
I want to lose a life when my ship collides with asteroids, saucers, or saucer bullets,
So that the game presents a real challenge.

**Acceptance Criteria:**

**Given** the ship is not invincible
**When** the ship overlaps an asteroid, saucer, or saucer bullet
**Then** the player loses one life (FR22)
**And** the ship's `alive` is set to `False`
**And** a ship death explosion is triggered

**Given** the ship has invincibility active (within 3 seconds of respawn)
**When** the ship overlaps any threat
**Then** no life is lost and no collision response occurs

---

## Epic 5: Game Loop Core

**Goal:** Implement the scoring system, lives management, respawn logic, and wave progression.

### Story 5.1: Score and Lives System

As a player,
I want my score to increase when I destroy enemies and earn extra lives at milestones,
So that I feel rewarded for skill.

**Acceptance Criteria:**

**Given** a player bullet destroys an asteroid
**When** the collision resolves
**Then** the score increases by the correct value (large: 20, medium: 50, small: 100)
**And** the HUD score display updates immediately

**Given** a player bullet destroys a saucer
**When** the collision resolves
**Then** score increases by 200 (large) or 1,000 (small)

**Given** the player's score passes a multiple of 10,000
**When** the score is updated
**Then** one extra life is awarded if current lives < 5
**And** a visual/audio indicator is triggered (FR23)

---

### Story 5.2: Respawn System

As a player,
I want to respawn at the center of the screen with temporary invincibility,
So that I have a fair chance to recover after dying.

**Acceptance Criteria:**

**Given** the ship has just been destroyed and lives > 0
**When** 2 seconds elapse
**Then** the ship spawns at screen center (if the 150 px safe zone is clear)
**And** if the zone is not clear, spawning is delayed until it is (FR25)

**Given** the ship has respawned
**When** the first 3 seconds of respawn elapse
**Then** the ship blinks by toggling visibility every 5 frames (FR26)
**And** no collision damage is applied during this period (FR26)
**And** the player can still fire during invincibility (FR27)

---

### Story 5.3: Wave Progression

As a player,
I want new waves of asteroids to appear after I clear the field,
So that the game continues to escalate in difficulty.

**Acceptance Criteria:**

**Given** all asteroids are destroyed and no saucer is active
**When** 2 seconds elapse
**Then** the next wave begins with the correct asteroid count (wave 1: 4, +1/wave, cap 12)
**And** "WAVE X" displays top-right for 3 seconds (FR30)

**Given** a wave number > 5
**When** asteroids spawn
**Then** their speed range is increased by ~5% per wave above wave 5 (FR32)

---

## Epic 6: Game States and UI

**Goal:** Implement the full state machine, pause system, HUD, title screen, and game over screen.

### Story 6.1: Full State Machine

As a developer,
I want a complete, explicit state machine in `main.py`,
So that all game states transition correctly with no undefined states.

**Acceptance Criteria:**

**Given** the game starts
**When** `main.py` initializes
**Then** state is `GameState.TITLE_SCREEN`

**Given** any `transition_to(new_state)` call
**When** a new state is requested
**Then** only valid transitions are accepted (TITLE→PLAYING, PLAYING→PAUSED, PLAYING→GAME_OVER, PAUSED→PLAYING, GAME_OVER→TITLE)
**And** entering each state triggers the appropriate setup logic

**Given** the player loses their last life
**When** the collision resolves
**Then** state transitions to `GameState.GAME_OVER` (FR37)

---

### Story 6.2: Pause System

As a player,
I want to pause and unpause the game at any time during play,
So that I can take breaks without quitting.

**Acceptance Criteria:**

**Given** the game is in `PLAYING` state
**When** the player presses Esc or P
**Then** state transitions to `PAUSED`
**And** all game object updates stop (physics, movement, collisions)
**And** a semi-transparent dark overlay with "PAUSED" text renders

**Given** the game is in `PAUSED` state
**When** the player presses Esc or P
**Then** state transitions back to `PLAYING`
**And** gameplay resumes from the exact paused moment

---

### Story 6.3: HUD

As a player,
I want to see my score, high score, lives, and wave number at all times during play,
So that I always know my game status.

**Acceptance Criteria:**

**Given** the game is in `PLAYING` state
**When** `hud.draw(screen)` is called
**Then** current score renders top-left in white (~28px font)
**And** all-time high score renders top-center (~22px font)
**And** remaining lives render as small ship icons below the score (top-left)
**And** "WAVE X" renders top-right for 3 seconds at the start of each wave

---

### Story 6.4: Title and Game Over Screens

As a player,
I want a title screen and game over screen,
So that the game has proper entry and exit points.

**Acceptance Criteria:**

**Given** the game is in `TITLE_SCREEN` state
**When** the screen renders
**Then** "ASTEROIDS" displays in large centered vector text
**And** "PRESS ENTER TO START" flashes (toggle every ~30 frames)
**And** the current high score displays below the title
**And** a few asteroids drift non-interactively in the background

**Given** the game is in `TITLE_SCREEN` state
**When** the player presses Enter
**Then** state transitions to `PLAYING` and Wave 1 begins

**Given** the game is in `GAME_OVER` state
**When** the screen renders
**Then** "GAME OVER" displays centered in large text
**And** the final score is shown
**And** "NEW HIGH SCORE!" displays if the current score exceeds the stored high score

**Given** the game is in `GAME_OVER` state
**When** the player presses Enter OR 10 seconds elapse
**Then** state transitions to `TITLE_SCREEN` (FR36)

---

## Epic 7: Advanced Gameplay

**Goal:** Implement high score persistence, enemy saucers, difficulty scaling, and hyperspace.

### Story 7.1: High Score Persistence

As a player,
I want my best score saved between sessions,
So that I have a long-term goal to beat.

**Acceptance Criteria:**

**Given** the game transitions to `GAME_OVER`
**When** the final score exceeds the stored high score
**Then** `highscore.save(score)` writes `{"high_score": N}` to `highscore.json`

**Given** the game starts
**When** `highscore.load()` is called
**Then** it returns the integer value from `highscore.json`
**And** if the file is missing, it returns `0` without crashing (NFR5)
**And** if the file is corrupt (invalid JSON), it returns `0` without crashing (NFR5)

---

### Story 7.2: Large Saucer

As a player,
I want a large enemy saucer to appear periodically and fire at me,
So that the game has an additional threat beyond asteroids.

**Acceptance Criteria:**

**Given** the game is in `PLAYING / ACTIVE` state
**When** the large saucer spawn timer expires (every 15–25 seconds initially)
**Then** one large saucer (~40 px) enters from a random vertical position on the left or right edge
**And** only one saucer can be on screen at a time (FR16)

**Given** a large saucer is on screen
**When** it moves
**Then** it travels horizontally, changing vertical direction randomly every 1–2 seconds
**And** it fires a bullet in a random direction every 1.5 seconds
**And** it wraps horizontally; despawns if it exits the top or bottom edge

**Given** a large saucer is destroyed
**When** the collision resolves
**Then** 200 points are awarded to the player (FR21)

---

### Story 7.3: Small Saucer and Difficulty Scaling

As a player,
I want the game to get harder as I score more points,
So that high-score runs remain challenging.

**Acceptance Criteria:**

**Given** the player's score exceeds 40,000
**When** the next saucer spawns
**Then** it is always a small saucer (~20 px) — no large saucers appear (FR33)

**Given** a small saucer is on screen
**When** it fires
**Then** it fires aimed shots toward the player with ±15° random offset every 1.0 second
**And** its bullet speed is 600 px/s
**And** destroying it awards 1,000 points

**Given** a wave number N > 1
**When** the saucer spawn timer is calculated
**Then** the interval is reduced by 1 second per wave (minimum 10 seconds) (FR31)

---

### Story 7.4: Saucer Bullets and Collisions

As a player,
I want saucer bullets to threaten me and also destroy asteroids,
So that saucers create chaotic danger in the field.

**Acceptance Criteria:**

**Given** a saucer fires a bullet
**When** the bullet is created
**Then** it travels at 500 px/s (large saucer) or 600 px/s (small saucer)
**And** it despawns after 1.5 seconds regardless of contact
**And** it wraps around screen edges

**Given** a saucer bullet overlaps the player ship (not invincible)
**When** the collision resolves
**Then** the player loses a life and the bullet is destroyed (FR22)

**Given** a saucer bullet overlaps an asteroid
**When** the collision resolves
**Then** the asteroid splits/destroys and the bullet is destroyed
**And** no points are awarded to the player (FR17)

---

### Story 7.5: Hyperspace

As a player,
I want to hyperspace-jump to a random screen position with a risk of death,
So that I have an emergency escape option with meaningful consequences.

**Acceptance Criteria:**

**Given** the game is in `PLAYING / ACTIVE` state and hyperspace cooldown is 0
**When** the player presses Left Shift (or H)
**Then** the ship teleports to a random screen position
**And** a 1-in-6 random check is performed; if triggered, the ship is destroyed as if it collided with an obstacle (FR7)
**And** the 2-second cooldown timer starts immediately (FR8)

**Given** the hyperspace cooldown is active (< 2 seconds since last use)
**When** the player presses the hyperspace key
**Then** nothing happens

---

## Epic 8: Audio

**Goal:** Implement the sound manager, all sound effects, saucer alarm, and the heartbeat system.

### Story 8.1: Sound Manager and Basic SFX

As a player,
I want sound effects for shooting, explosions, death, and other events,
So that the game feels responsive and satisfying.

**Acceptance Criteria:**

**Given** `SoundManager.__init__()` is called
**When** any sound file is missing or fails to load
**Then** that sound is set to `None` and no exception is raised (NFR4)

**Given** `SoundManager.play(sound)` is called
**When** `sound` is `None`
**Then** nothing happens (silent skip, no crash)
**When** `sound` is a valid `pygame.mixer.Sound`
**Then** the sound plays once

**Given** the following events occur in gameplay
**Then** the corresponding sounds play:
- Player fires bullet → fire sound
- Small asteroid destroyed → small explosion sound
- Medium asteroid destroyed → medium explosion sound
- Large asteroid destroyed → large explosion sound
- Ship destroyed → ship death sound
- Hyperspace activated → hyperspace sound

---

### Story 8.2: Saucer Alarm and Heartbeat

As a player,
I want a looping saucer alarm while a saucer is present, and a tempo-based heartbeat that speeds up,
So that I feel increasing tension as the wave progresses.

**Acceptance Criteria:**

**Given** a saucer enters the screen
**When** it becomes active
**Then** the saucer alarm starts looping (large saucer pitch ≠ small saucer pitch) (FR40)

**Given** the saucer is destroyed or exits the screen
**When** it is removed
**Then** the saucer alarm stops

**Given** the game is in `PLAYING / ACTIVE` state
**When** the heartbeat plays
**Then** the beat interval = `1.0 / lerp(1, 4, 1 - (remaining_asteroids / total_asteroids))` seconds approximately
**And** with many asteroids: ~1 beat/second; with few asteroids: ~4 beats/second (FR41)

---

## Epic 9: Visual Polish

**Goal:** Implement explosion particle effects, edge-wrapping visual fix, and extra life indicator.

### Story 9.1: Explosion Particles

As a player,
I want asteroid and ship explosions to show line-segment debris scattering outward,
So that destruction feels visually satisfying.

**Acceptance Criteria:**

**Given** an asteroid (any size) is destroyed
**When** the destruction triggers
**Then** 4–8 line-segment debris particles spawn at the asteroid's position
**And** each particle moves outward at a random angle and speed
**And** particles fade out and are removed after 0.5 seconds

**Given** the ship is destroyed
**When** the destruction triggers
**Then** 4–6 line-segment debris particles spawn
**And** particles fade and are removed after 1.0 seconds

**Given** a saucer is destroyed
**When** the destruction triggers
**Then** similar particle debris spawns and fades after 0.5 seconds

---

### Story 9.2: Screen Edge Visual Continuity

As a player,
I want objects near screen edges to appear on both sides simultaneously,
So that wrapping feels seamless with no visual pop.

**Acceptance Criteria:**

**Given** any game object's center is within one `radius` of a screen edge
**When** `draw(screen)` is called
**Then** the object is drawn at its current position AND at the mirrored position on the opposite edge
**And** this applies to ships, bullets, asteroids, and saucers

---

### Story 9.3: Extra Life Indicator

As a player,
I want a visual and audio indicator when I earn an extra life,
So that I don't miss this important game event.

**Acceptance Criteria:**

**Given** the player's score crosses a 10,000-point threshold and lives < 5
**When** the extra life is awarded
**Then** the extra life sound plays
**And** the lives HUD icon count increases by 1 immediately
**And** a brief on-screen text flash "1UP" or similar displays for ~1 second

---

## Epic 10: Integration and Acceptance Testing

**Goal:** Verify all 52 FRs and 6 NFRs pass with manual testing, and the complete game plays end-to-end without bugs.

### Story 10.1: Full Integration Test Pass

As a developer,
I want to verify all acceptance criteria from the PRD are met,
So that the v1.0 release is confirmed complete and correct.

**Acceptance Criteria:**

**Given** all previous epics are implemented
**When** a manual test session runs through all 14 PRD acceptance criteria
**Then** all 14 pass with no failures

**Given** a 30-minute continuous play session
**When** the session runs with deliberate stress (rapid firing, hyperspace spam, high wave numbers)
**Then** zero crashes, soft-locks, or corrupted state occur

**Given** the `tests/` directory
**When** `pytest` is run from the project root
**Then** all unit tests pass: `test_utils.py`, `test_ship.py`, `test_asteroid.py`, `test_collision.py`, `test_highscore.py`, `test_sounds.py`

**Given** the game is run with all sound files removed from `assets/sounds/`
**When** the game launches and plays through a full session
**Then** no exceptions are raised and gameplay functions normally (NFR4)

**Given** `highscore.json` is deleted before launch
**When** the game starts and ends (game over)
**Then** high score defaults to 0 on load and a new `highscore.json` is created on save (NFR5)
