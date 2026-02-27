# Story 2.3 — Controller Input Baseline

## Context
Players should be able to use a gamepad for core actions without losing keyboard support.

## User Story
As a player, I want basic gamepad controls so I can play Asteroids with a controller.

## Tasks
- [x] Detect controller connect/disconnect events and show status hints.
- [x] Add baseline mapping:
  - Left stick X-axis → turn
  - A button → thrust
  - B button / RT axis → fire
  - Start button → pause
- [x] Implement deadzone handling for analog input.
- [x] Keep keyboard input functional when no controller is connected.
- [x] Add fire/pause debounce to avoid rapid accidental repeats.

## Acceptance Criteria
- Controller connect/disconnect is handled and surfaced to player.
- Core game actions work with connected gamepad.
- Analog deadzone prevents drift.
- Keyboard controls continue to work in all states.

## Notes
- Uses pygame joystick API with first connected controller.
- Controller handling is active only during `PLAYING + ACTIVE` substate.
