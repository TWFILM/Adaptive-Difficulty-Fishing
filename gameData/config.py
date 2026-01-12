# config.py
WIDTH, HEIGHT = 600, 800    # BASE W, H

BG_COLOR = (20, 30, 40)
BAR_COLOR = (100, 255, 100)
FISH_COLOR = (255, 80, 80)

BAR_HEIGHT = 50          # FIXED height
BAR_WIDTH = 120     # FIXED width (NO AUTO CHANGE)
BAR_MIN_X = 10
BAR_MAX_X = WIDTH - 150


FISH_SIZE = 20
FPS = 60

TRACK_HEIGHT = 50
TRACK_Y = HEIGHT - 200   # bottom bar location Y
TRACK_COLOR = (30, 45, 60)
CONTROLLED = -0.2

FISH_MOVE_MIN_DIST = 40
FISH_MOVE_MAX_DIST = 160
FISH_MIN_SPEED = 0.5    # spd const
FISH_MAX_SPEED = 3.0    # spd const
FISH_RESILIENCE = -0.7  # high = slower (not use bc move it to the fish_data)

PROGRESS_INIT = 0.2
PROGRESS_FILL_ANIM_SPEED = 0.007


PROGRESS_UP_RATE = 0.002     # cacthing
PROGRESS_DOWN_RATE = 0.003   # miss

PROGRESS_BAR_WIDTH = 300
PROGRESS_BAR_HEIGHT = 16
PROGRESS_BAR_Y = TRACK_Y + 75   # progression bar location y

ENCOUNTER_FREEZE_TIME = 2   # sec

BAR_MAX_SPEED = 8.0       # Limit
BAR_FRICTION = 0.96       # inertia control

BAR_FORCE_INC = 0.04     # increase when mouse clicked
BAR_FORCE_DEC = 0.05    # decrease when mouse is not clicked
BAR_FORCE_MAX = 0.9      

BAR_DRIFT_LEFT = -0.5
