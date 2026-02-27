# Story 2.2 — Pause/Resume UX & Fullscreen Polish

## Context
Pause interactions need to be clear and complete, and fullscreen should be toggleable with visible state.

## User Story
As a player, I want a reliable pause menu and fullscreen toggle so game flow feels polished.

## Tasks
- [x] Add pause menu options: Resume, Restart, Settings, Fullscreen, Quit.
- [x] Support up/down + enter menu navigation.
- [x] Keep Escape/Pause key toggle behavior reliable.
- [x] Implement fullscreen toggle function and display mode refresh.
- [x] Reflect fullscreen ON/OFF state in pause menu label.
- [x] Keep gameplay updates frozen while paused/settings states are active.

## Acceptance Criteria
- Pause overlay includes all expected options.
- Escape toggles pause reliably.
- Fullscreen toggle is available and state is reflected.
- No gameplay input/update bleed while paused/settings overlays are shown.

## Notes
- Added global display mode manager and `_toggle_fullscreen()` helper.
- Added `F` hotkey support in title/playing states.
