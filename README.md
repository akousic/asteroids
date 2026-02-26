# Asteroids (Pygame Clone)

A faithful recreation of the 1979 Atari Asteroids arcade game, built with Python 3 and Pygame 2.

## Requirements

- Python 3.8 or higher
- Pygame 2.x

## Setup

### macOS / Linux

```bash
# Clone or navigate to the project directory
cd asteroids

# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows

```bat
cd asteroids

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

A 1280×720 black window will open. Press **Escape** or close the window to quit.

## Controls

| Key | Action |
|---|---|
| W / Up Arrow | Thrust |
| A / Left Arrow | Rotate left |
| D / Right Arrow | Rotate right |
| Space | Fire |
| Left Shift / H | Hyperspace |
| Esc / P | Pause |
| Enter | Start game (from title) |

## Running Tests

```bash
pytest
```

## Project Structure

```
asteroids/
├── main.py          # Game loop and state machine
├── settings.py      # All constants
├── ship.py          # Player ship (added in Epic 2)
├── asteroid.py      # Asteroids (added in Epic 3)
├── bullet.py        # Bullets (added in Epic 2)
├── saucer.py        # Enemy saucers (added in Epic 7)
├── particle.py      # Explosion effects (added in Epic 9)
├── hud.py           # HUD rendering (added in Epic 6)
├── menu.py          # Title/game-over screens (added in Epic 6)
├── highscore.py     # Score persistence (added in Epic 7)
├── sounds.py        # Sound manager (added in Epic 8)
├── utils.py         # Shared math utilities (added in Epic 1)
├── assets/
│   └── sounds/      # Audio files (added in Epic 8)
├── tests/           # Unit tests
├── requirements.txt
└── highscore.json   # Auto-created at first game over
```
