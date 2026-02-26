# ──────────────────────────────────────────────
# SCREEN
# ──────────────────────────────────────────────
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60

# ──────────────────────────────────────────────
# PHYSICS (populated fully in Story 2.1)
# ──────────────────────────────────────────────
DRAG_COEFFICIENT = 0.98       # velocity multiplier per frame
SHIP_THRUST      = 300.0      # px/s² acceleration
MAX_SPEED        = 600.0      # px/s velocity cap
ROTATION_SPEED   = 270.0      # degrees/second

# ──────────────────────────────────────────────
# BULLETS (populated in Story 2.2)
# ──────────────────────────────────────────────
BULLET_SPEED    = 800.0       # px/s
BULLET_LIFETIME = 1.0         # seconds
MAX_BULLETS     = 4           # max simultaneous player bullets

# ──────────────────────────────────────────────
# ASTEROIDS (populated in Story 3.1)
# ──────────────────────────────────────────────
ASTEROID_LARGE_RADIUS  = 50
ASTEROID_MEDIUM_RADIUS = 25
ASTEROID_SMALL_RADIUS  = 12

ASTEROID_LARGE_SPEED_MIN  = 40.0
ASTEROID_LARGE_SPEED_MAX  = 80.0
ASTEROID_MEDIUM_SPEED_MIN = 80.0
ASTEROID_MEDIUM_SPEED_MAX = 140.0
ASTEROID_SMALL_SPEED_MIN  = 140.0
ASTEROID_SMALL_SPEED_MAX  = 220.0

ASTEROID_SPAWN_SAFE_RADIUS = 150  # px from player at wave start

# ──────────────────────────────────────────────
# SCORING
# ──────────────────────────────────────────────
SCORE_LARGE_ASTEROID  = 20
SCORE_MEDIUM_ASTEROID = 50
SCORE_SMALL_ASTEROID  = 100
SCORE_LARGE_SAUCER    = 200
SCORE_SMALL_SAUCER    = 1000
EXTRA_LIFE_THRESHOLD  = 10000   # points per extra life
MAX_LIVES             = 5

# ──────────────────────────────────────────────
# RESPAWN
# ──────────────────────────────────────────────
RESPAWN_DELAY       = 2.0     # seconds after death
INVINCIBILITY_TIME  = 3.0     # seconds of post-respawn invincibility
BLINK_RATE          = 5       # frames per blink toggle
RESPAWN_SAFE_RADIUS = 150     # px from center spawn point

# ──────────────────────────────────────────────
# WAVE
# ──────────────────────────────────────────────
WAVE_ASTEROID_START   = 4     # large asteroids in wave 1
WAVE_ASTEROID_MAX     = 12    # cap from wave 6+
WAVE_TRANSITION_DELAY = 2.0   # seconds before next wave starts
WAVE_BANNER_DURATION  = 3.0   # seconds to show "WAVE X"

# ──────────────────────────────────────────────
# SAUCER
# ──────────────────────────────────────────────
SAUCER_SPAWN_INTERVAL_BASE    = 15.0  # seconds between spawns (wave 1)
SAUCER_SPAWN_INTERVAL_MIN     = 10.0  # minimum interval floor
SAUCER_LARGE_RADIUS           = 20    # px
SAUCER_SMALL_RADIUS           = 10    # px
SAUCER_LARGE_FIRE_INTERVAL    = 1.5   # seconds between shots
SAUCER_SMALL_FIRE_INTERVAL    = 1.0
SAUCER_AIM_SPREAD             = 15.0  # degrees of random offset on aimed shot
SMALL_SAUCER_SCORE_THRESHOLD  = 40000 # score at which only small saucers spawn

# ──────────────────────────────────────────────
# HYPERSPACE
# ──────────────────────────────────────────────
HYPERSPACE_DEATH_CHANCE = 1 / 6
HYPERSPACE_COOLDOWN     = 2.0  # seconds

# ──────────────────────────────────────────────
# COLORS
# ──────────────────────────────────────────────
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)

# ──────────────────────────────────────────────
# RENDERING
# ──────────────────────────────────────────────
LINE_WIDTH = 2  # polygon stroke width in px
