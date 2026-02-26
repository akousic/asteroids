---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain-skipped
  - step-06-innovation-skipped
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-12-complete
classification:
  projectType: desktop_app
  domain: general
  complexity: medium
  projectContext: brownfield
inputDocuments:
  - '/Users/kousic/Desktop/learn/bmad/asteroids-prd.md'
workflowType: 'prd'
briefCount: 0
researchCount: 0
brainstormingCount: 0
projectDocsCount: 1
---

# Product Requirements Document — Asteroids (Pygame Clone)

**Author:** Kousic
**Date:** 2026-02-25

---

## Executive Summary

Asteroids (Pygame Clone) is a faithful PC recreation of Atari's 1979 vector-graphics arcade game, implemented in Python 3.x and Pygame with no additional engine dependencies. The product delivers the complete original gameplay loop — thrust-and-shoot physics, asteroid splitting, enemy saucers, progressive wave difficulty, and hyperspace — at a locked 60 FPS with vector-line aesthetics on a 1280×720 display. Target audience: PC players on Windows, macOS, and Linux who value authentic arcade gameplay, and Python developers seeking a clean reference implementation of a complete game system.

### What Makes This Special

A strict no-engine constraint forces every subsystem — Newtonian physics, circular collision detection, delta-time movement, procedural polygon generation, state machine, audio management, and high score persistence — to be built directly in Pygame. This produces a self-contained, dependency-minimal codebase that is both a playable authentic Asteroids experience and a readable architecture reference. The two-tone heartbeat tempo system, saucer aim logic, hyperspace risk mechanic, and respawn safe-zone handling reproduce the original's tension and risk/reward dynamics with precision.

## Project Classification

| Property | Value |
|---|---|
| Project Type | Desktop Application (Python 3.x + Pygame) |
| Domain | General Software |
| Complexity | Medium — game physics, collision, state machine, audio, persistence |
| Project Context | Brownfield — structured from existing PRD v1.0 |
| Platform | Windows / macOS / Linux |

---

## Success Criteria

### User Success

- Player completes a full session (title → wave 1 → death → game over → title) without crashes or unintended behavior
- Controls respond within the same frame as input — rotation, thrust, and firing feel instantaneous
- Ship retains momentum on thrust release; asteroids split convincingly; hyperspace carries real risk
- Respawn safe-zone logic prevents instant-death collisions immediately after re-entry
- High score persists correctly between sessions; players can track improvement over time

### Business Success

- Codebase serves as a clean, dependency-minimal Python/Pygame reference suitable for portfolio or education
- All 14 acceptance criteria from the source PRD pass manual verification at v1.0 release
- Zero external dependencies beyond Python 3.8+ and Pygame 2.x

### Technical Success

- Stable 60 FPS with 30+ simultaneous game objects on screen
- Delta-time physics produces consistent behavior across hardware speeds
- All 6 collision type combinations register correctly — zero false positives or missed detections
- Missing audio files do not crash the game; audio is skipped gracefully
- Missing or corrupt `highscore.json` defaults to 0 without crashing

### Measurable Outcomes

- All 14 acceptance criteria pass manual test verification before v1.0 tag
- Zero game-breaking bugs (crashes, soft-locks, corrupted state) during a 30-minute continuous play session
- New player can complete Wave 1 within 10 minutes of first launch

---

## Product Scope

### MVP — Minimum Viable Product

Ship thrust/rotation/fire controls, screen-wrapping movement, 3 asteroid sizes with splitting behavior, player bullets (max 4 simultaneous), circular collision detection, lives system (start 3, max 5), score tracking, wave progression (clear all → next wave), game over state, high score persistence to `highscore.json`, HUD (score/lives/wave), title screen, game over screen, thrust flame visual, respawn invincibility blink, death explosion debris particles.

### Growth Features (Post-MVP)

Enemy saucers (large and small) with distinct firing behavior, saucer bullets, hyperspace mechanic with 1-in-6 destruction risk and 2-second cooldown, background heartbeat audio with tempo scaling, full sound effects suite (thrust loop, fire, explosions by size, saucer alarm, extra life, hyperspace), pause screen, fullscreen toggle (F11), asteroid and saucer explosion debris animations, per-wave asteroid speed scaling, saucer spawn frequency scaling.

### Vision (Future)

Local multiplayer, gamepad/controller support, settings menu (key rebinding, volume, resolution), online leaderboard, custom wave configurations, mobile/web builds.

---

## User Journeys

### Journey 1: The Casual Player — First Session (Primary User, Success Path)

**Persona:** Alex, a developer who remembers Asteroids from the arcade but hasn't played in years.

- **Opening Scene:** Alex launches the game (`python main.py`). The title screen appears: "ASTEROIDS" in large vector text, high score 0, asteroids drifting in the background. Alex presses Enter.
- **Rising Action:** Wave 1 begins. Pressing W thrusts the ship forward — it keeps drifting when W is released. Alex rotates with A/D, fires with Space, and destroys a large asteroid. It splits into two mediums that scatter in opposite directions. The familiar feel clicks immediately.
- **Climax:** Alex clears Wave 1. "WAVE 2" flashes top-right. A saucer warbles in from the right edge — Alex destroys it for 200 points. The heartbeat bass tone quickens.
- **Resolution:** Alex dies on Wave 3. The game over screen shows their score. They press Enter, return to the title screen, and see the score saved as the new high score. "I'll beat that tomorrow."

**Reveals:** Title screen, wave transition, asteroid splitting, saucer behavior, HUD, game over, high score save.

---

### Journey 2: The Score Chaser — High Score Attempt (Primary User, Edge Case)

**Persona:** Morgan, a competitive player chasing a personal best across repeated sessions.

- **Opening Scene:** Morgan launches the game. Their previous high score of 34,200 is displayed. The goal: beat it.
- **Rising Action:** Morgan uses hyperspace strategically to escape tight situations. On Wave 7, the ship materializes inside an asteroid — the 1-in-6 destruction chance triggers. Ship dies. Morgan respawns with 3-second invincibility, using the blink period to assess the field before moving.
- **Climax:** At 41,000 points, only small saucers spawn — aimed shots within ±15°. Morgan destroys one for 1,000 points. The heartbeat is at near-maximum tempo.
- **Resolution:** Morgan reaches 52,500 — a new high score. "NEW HIGH SCORE!" displays on game over. Score writes to `highscore.json`. Next session will show it as the target.

**Reveals:** Hyperspace risk, respawn safe-zone timing, small saucer aimed behavior, extra life awards, high score persistence, max lives cap.

---

### Journey 3: The Python Developer — Code Study (Secondary User)

**Persona:** Sam, a CS student learning Python game development, reading the codebase as a reference.

- **Opening Scene:** Sam opens `main.py` to understand the entry point and game loop structure.
- **Rising Action:** Sam traces `update(dt)` — discovers delta-time physics, safe list iteration during object removal, the rotation matrix applied to polygon vertices, and sum-of-radii collision detection.
- **Climax:** Sam tweaks `settings.py` (adjusting `MAX_BULLETS` or `ROTATION_SPEED`), runs the game, and observes the effect immediately. Constants isolation makes experimentation safe and contained.
- **Resolution:** Sam understands how a complete state machine (TITLE → PLAYING → PAUSED → GAME_OVER) is implemented cleanly without a framework. The project becomes a template for their own work.

**Reveals:** Settings isolation, clean file structure, delta-time pattern, state machine design, object list management.

### Journey Requirements Summary

| Journey | Capabilities Revealed |
|---|---|
| Casual Player | Title screen, wave transitions, asteroid physics, saucer, HUD, game over, high score |
| Score Chaser | Hyperspace risk, respawn safe-zone, saucer difficulty scaling, extra lives, score persistence |
| Developer | Settings isolation, file structure, delta-time, state machine, list management patterns |

---

## Desktop Application Requirements

### Platform Support

| Platform | Target | Notes |
|---|---|---|
| Windows 10/11 | Primary | Python 3.8+ + Pygame 2.x via pip |
| macOS 12+ | Supported | Standard Python/Pygame install |
| Linux (Ubuntu 20.04+) | Supported | Standard Python/Pygame install |

### System Integration

No OS-level system integration required. Reads/writes a single local file (`highscore.json`) in the game directory. No network access, external APIs, or OS services.

### Update Strategy

No auto-update mechanism — v1.0 is a complete, self-contained release. Distributed as source code; player installs via `pip install pygame` and runs `python main.py`.

### Offline Capabilities

Fully offline — no internet connection required at any point. All assets (source code, sound files) bundled with the distribution.

---

## Functional Requirements

### Ship Control & Physics

- FR1: Player can rotate the ship left/right continuously while keys are held (270°/second)
- FR2: Player can apply thrust in the ship's facing direction, accumulating velocity
- FR3: Ship velocity decays by drag coefficient ×0.98 per frame when thrust is not applied
- FR4: Ship velocity is clamped to a maximum of 600 px/s
- FR5: Player can fire one bullet per key press in the ship's facing direction (Space key)
- FR6: Player can activate hyperspace to teleport the ship to a random screen position
- FR7: Hyperspace carries a 1-in-6 probability of destroying the ship on re-entry
- FR8: Hyperspace has a 2-second cooldown between activations
- FR9: Player can pause and unpause the game (Esc or P)

### Game Objects & Behavior

- FR10: Asteroids spawn at random screen edge positions at wave start, at least 150 px from the player
- FR11: Large and medium asteroids split into 2 smaller asteroids on destruction; small asteroids are destroyed outright
- FR12: Child asteroids inherit parent position and travel at parent angle ±20–60° random offset
- FR13: All game objects (ship, bullets, asteroids, saucers) wrap around all four screen edges
- FR14: Large saucer spawns on a timed interval, moves horizontally with random vertical direction changes every 1–2 seconds, fires randomly every 1.5 seconds
- FR15: Small saucer spawns after player reaches 40,000 points, fires aimed shots toward player with ±15° random offset every 1.0 second
- FR16: At most one saucer is on screen at any time
- FR17: Saucer bullets can destroy asteroids and the player ship
- FR18: Player bullets are destroyed on contact with asteroids or saucers; max 4 player bullets on screen simultaneously
- FR19: Player bullets despawn after 1.0 seconds regardless of contact

### Collision & Scoring

- FR20: Player earns points when a bullet destroys an asteroid (large: 20 / medium: 50 / small: 100)
- FR21: Player earns points when a bullet destroys a saucer (large: 200 / small: 1,000)
- FR22: Player loses a life when the ship collides with an asteroid, saucer, or saucer bullet
- FR23: Player earns one extra life at every 10,000 points; lives are capped at 5

### Respawn & Invincibility

- FR24: Ship respawns at screen center after a 2-second delay following death
- FR25: Respawn is delayed while any asteroid is within 150 px of the center spawn point
- FR26: Ship has 3 seconds of collision invincibility after respawning; ship blinks (toggle every 5 frames) to signal this state
- FR27: Player can fire during the invincibility period

### Wave & Difficulty Progression

- FR28: Each wave begins with a set count of large asteroids (wave 1: 4, +1/wave, capped at 12 from wave 6+)
- FR29: Next wave begins after a 2-second pause once all asteroids are destroyed and no saucer is active
- FR30: "WAVE X" is displayed in the top-right for 3 seconds at wave start
- FR31: Saucer spawn interval decreases by 1 second per wave (minimum 10 seconds)
- FR32: Asteroid speed range increases ~5% per wave after wave 5
- FR33: Only small saucers spawn once the player exceeds 40,000 points

### Game State Management

- FR34: Game transitions correctly through all states: TITLE_SCREEN → PLAYING → PAUSED → GAME_OVER → TITLE_SCREEN
- FR35: Sub-states RESPAWNING and WAVE_TRANSITION operate within PLAYING without breaking outer state flow
- FR36: Game over screen returns to title on Enter key press or after a 10-second auto-timeout
- FR37: Game over triggers when the player loses their last life

### Audio

- FR38: Thrust sound loops while the thrust key is held and stops when released
- FR39: Distinct sound effects play for: bullet fire, asteroid explosion (per size), ship death, saucer destruction, extra life awarded, hyperspace activation
- FR40: Saucer alarm loops while a saucer is on screen; large and small saucers use different pitches
- FR41: Background heartbeat tempo scales from ~1 beat/second (many asteroids) to ~4 beats/second (few asteroids remaining)
- FR42: Missing audio files do not crash the game; audio events are silently skipped

### Visual Rendering & HUD

- FR43: All game objects render as white vector-line polygons (2 px line width) on a black background at 60 FPS
- FR44: Each asteroid instance is a procedurally generated irregular polygon (8–12 vertices, radii ±30% of base radius)
- FR45: Thrust flame renders as a flickering triangle at the ship's rear when thrusting (toggles every 3–4 frames)
- FR46: Explosion animations render as line-segment debris that scatter outward and fade (asteroids: 0.5 s, ship: 1.0 s, saucer: 0.5 s)
- FR47: Objects near screen edges render at both the current and wrapped opposite position to prevent visual pop
- FR48: HUD displays: current score (top-left, ~28px), high score (top-center, ~22px), ship-icon lives (top-left below score), wave number (top-right, 3 s at wave start)
- FR49: Title screen shows game title, flashing "PRESS ENTER TO START", current high score, and non-interactive drifting asteroids
- FR50: Game over screen shows final score and "NEW HIGH SCORE!" when applicable

### Persistence

- FR51: High score is written to `highscore.json` at game over
- FR52: High score is read from `highscore.json` at startup; missing or corrupt file defaults to 0 without crashing

---

## Non-Functional Requirements

### Performance

- The game shall maintain 60 FPS as enforced by `pygame.Clock.tick(60)` with 30+ simultaneous active objects on screen
- All physics and movement calculations shall use delta time (dt in seconds) to ensure frame-rate-independent behavior across hardware
- Collision detection shall complete within a single frame budget (≤16.6 ms) for all active object pairs in a worst-case wave scenario

### Reliability

- Audio manager shall catch `pygame.error` and `FileNotFoundError` on sound load and continue silently — no missing sound file may raise an unhandled exception to the player
- Persistence layer shall catch `FileNotFoundError`, `json.JSONDecodeError`, and `PermissionError` on `highscore.json` read/write, defaulting to score 0 and continuing without interruption
- All game state transitions shall be explicitly enumerated — no game state shall be reachable without a defined transition path, preventing undefined behavior

---

*The Functional Requirements above constitute the capability contract for this product. UX design, architecture, and implementation must trace back to these requirements. Any capability not listed here is explicitly out of scope for v1.0.*
