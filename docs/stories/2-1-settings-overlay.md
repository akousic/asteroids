# Story 2.1 — Settings Overlay (Audio + Controls)

## Context
Players need in-game settings to tune audio and controls without editing code/config.

## User Story
As a player, I want a settings overlay so I can adjust sound and keybindings quickly.

## Tasks
- Add settings button entry points (main menu + pause overlay).
- Build settings modal component with tabs:
  - Audio
  - Controls
- Audio settings:
  - Master volume
  - Music volume
  - SFX volume
  - Persist to local storage
- Controls settings:
  - Rebind thrust/turn-left/turn-right/fire/pause
  - Detect duplicate bindings and block save
  - Reset defaults
- Add save/apply/cancel flow.
- Add unit/integration checks for persistence + conflict handling.

## Acceptance Criteria
- Settings opens from both menu and pause.
- Values persist after page refresh.
- Duplicate keybinds are prevented with user feedback.
- Reset restores defaults.

## Test Notes
- Verify bindings after reload.
- Verify pause key can still be used after rebind.
- Verify audio sliders affect runtime mix immediately.
