# BMAD Sprint A — Post‑MVP Quality & UX

## Goal
Improve playability and polish of the current Asteroids build without changing the core game loop.

## BMAD Scope
- **Business**: Increase replayability and reduce user friction.
- **Model**: Keep current game state model; add lightweight settings/profile state.
- **Architecture**: Add modular UI overlays and input abstraction where needed.
- **Delivery**: 3 stories, each independently shippable.

## Stories

### Story 2.1 — Settings Overlay (Audio + Controls)
**Outcome:** Player can open settings from pause/menu and adjust volume + keybinds.

**Acceptance Criteria**
- Settings overlay accessible from pause and main menu.
- Master/music/sfx sliders persist between sessions.
- Key rebind UI for thrust/turn/fire/pause with conflict validation.
- Reset-to-default button.

---

### Story 2.2 — Pause/Resume UX & Fullscreen Polish
**Outcome:** Pause feels clean and predictable across keyboard/mouse.

**Acceptance Criteria**
- Pause overlay includes Resume, Restart, Settings, Quit.
- Escape toggles pause reliably.
- Fullscreen toggle available and state reflected in UI.
- No input bleed while paused.

---

### Story 2.3 — Controller Input Baseline
**Outcome:** Basic gamepad support for move/turn/fire/pause.

**Acceptance Criteria**
- Detect gamepad connect/disconnect and show status hint.
- Default mapping for thrust/turn/fire/pause.
- Deadzone handling for analog stick.
- Keyboard still works when no controller connected.

## Non-Goals (Sprint A)
- Networking/multiplayer
- Online leaderboard backend
- New enemy archetypes or campaign mode

## Definition of Done
- All story acceptance criteria pass.
- Manual playtest checklist completed.
- No regressions in existing controls or scoring.
- Release notes updated.
