# config.py (This is the default version of config)

# ── SCREEN ─────────────────────────
WIDTH, HEIGHT = 600, 800    # FIXED SIZE

BG_COLOR = (20, 30, 40)
BAR_COLOR = (100, 255, 100)
FISH_COLOR = (255, 80, 80)
TRACK_COLOR = (30, 45, 60)

# ── TRACK (HORIZONTAL) ─────────────
TRACK_WIDTH = int(WIDTH * 0.85)
TRACK_HEIGHT = 58

TRACK_X = WIDTH // 2 - TRACK_WIDTH // 2
TRACK_Y = HEIGHT - 200   

# ── PLAYER BAR ─────────────────────
BAR_WIDTH = 120     # FIXED width (NO AUTO CHANGE)
BAR_HEIGHT = TRACK_HEIGHT

BAR_MIN_X = TRACK_X
BAR_MAX_X = TRACK_X + TRACK_WIDTH - BAR_WIDTH

# ── FISH ───────────────────────────
FISH_SIZE = 20

# ── PROGRESS BAR ───────────────────
PROGRESS_BAR_WIDTH = int(TRACK_WIDTH * 0.6)
PROGRESS_BAR_HEIGHT = 16
PROGRESS_BAR_Y = TRACK_Y + TRACK_HEIGHT + 25
PROGRESS_BAR_COLOR = (255, 255, 255)

PROGRESS_INIT = 0.25
PROGRESS_FILL_ANIM_SPEED = 0.007
PROGRESS_UP_RATE = 0.002        # catching
PROGRESS_DOWN_RATE = 0.002      # miss

# ── PHYSICS ─────────────────────────
FPS = 60

BAR_MAX_SPEED = 8.0
BAR_FRICTION = 0.94             # inertia control

BAR_FORCE_INC = 0.03            # spd increase when mouse clicked
BAR_FORCE_DEC = 0.03            # spd decrease when mouse is not
BAR_FORCE_MAX = 0.9

# pull bar LEFT
BAR_DRIFT_LEFT = -0.5

# ── FISH MOVEMENT ───────────────────
FISH_MOVE_MIN_DIST = 40
FISH_MOVE_MAX_DIST = 160
FISH_MIN_SPEED = 0.5
FISH_MAX_SPEED = 3.0
FISH_RESILIENCE = -0.7          # it is now moved to fish_data

ENCOUNTER_FREEZE_TIME = 2       # sec
