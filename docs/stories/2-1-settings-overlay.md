# Story 2.1 — Settings Overlay (Audio + Controls)

## Context
Players need in-game settings to tune audio and controls without editing code/config.

## User Story
As a player, I want a settings overlay so I can adjust sound and keybindings quickly.

## Tasks
- [x] Add settings entry points (title key `S` + pause overlay menu).
- [x] Build settings modal component with tabs:
  - [x] Audio
  - [x] Controls
- [x] Audio settings:
  - [x] Master volume
  - [x] Music volume
  - [x] SFX volume
  - [x] Persist to local storage
- [x] Controls settings:
  - [x] Rebind thrust/turn-left/turn-right/fire/pause
  - [x] Detect duplicate bindings and block save
  - [x] Reset defaults
- [x] Add save/apply/cancel flow.
- [x] Add sanity validation via Python compile check for touched modules.

## Acceptance Criteria
- Settings opens from both menu and pause.
- Values persist after page refresh.
- Duplicate keybinds are prevented with user feedback.
- Reset restores defaults.

## Test Notes
- Verify bindings after reload.
- Verify pause key can still be used after rebind.
- Verify audio sliders affect runtime mix immediately.
