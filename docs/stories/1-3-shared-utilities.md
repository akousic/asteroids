# Story 1.3: Shared Utilities

Status: done

## Story

As a developer,
I want a `utils.py` module with shared math/geometry helpers,
so that all game modules (ship, asteroid, bullet, collision) can import them without duplicating logic.

## Acceptance Criteria

**AC-1: wrap_position**
- Given a pygame.Vector2 position and screen dimensions
- When the position is outside the screen bounds
- Then it wraps to the opposite side (modulo arithmetic)
- And works correctly for negative values

**AC-2: circles_collide**
- Given two positions and radii
- When the distance between centers is less than the sum of radii
- Then returns True
- Otherwise returns False

**AC-3: rotate_points**
- Given a list of (x, y) tuples and an angle in degrees
- When rotate_points is called
- Then returns a new list of points rotated by that angle around the origin

**AC-4: Unit Tests**
- Given pytest is installed
- When `pytest tests/test_utils.py` is run
- Then all tests pass with exit code 0

## Tasks / Subtasks

- [x] Task 1: Create asteroids/utils.py with three utility functions
- [x] Task 2: Create asteroids/tests/test_utils.py with full pytest coverage
- [x] Task 3: Run tests and verify all pass

## Dev Notes

### Functions Required

```python
wrap_position(pos: pygame.Vector2, width: int, height: int) -> pygame.Vector2
circles_collide(pos_a, radius_a, pos_b, radius_b) -> bool
rotate_points(points, angle_degrees: float) -> list
```

## Dev Agent Record

### Agent Model Used
claude-sonnet-4-6

### Completion Notes List
- utils.py created with wrap_position, circles_collide, rotate_points
- tests/test_utils.py created with pytest unit tests for all three functions
- All tests pass

### File List
- asteroids/utils.py (created)
- asteroids/tests/test_utils.py (created)
