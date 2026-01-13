import pygame
import gameData.config as H
import gameData.config_vertical as V


class ScaledConfig:
    pass


def build_scaled_config(use_default="horizontal"):
    info = pygame.display.Info()

    base = H if use_default == "horizontal" else V

    scale = min(
        info.current_w / base.WIDTH,
        info.current_h / base.HEIGHT
    )

    s = ScaledConfig()
    

    # screen
    s.WIDTH = int(base.WIDTH * scale)
    s.HEIGHT = int(base.HEIGHT * scale)

    # bar
    s.BAR_WIDTH = int(base.BAR_WIDTH * scale)
    s.BAR_HEIGHT = int(base.BAR_HEIGHT * scale)

    if use_default == "horizontal":
        s.BAR_MIN_X = int(base.BAR_MIN_X * scale)
        s.BAR_MAX_X = s.WIDTH - s.BAR_WIDTH - s.BAR_MIN_X
    else:
        s.BAR_MIN_Y = int(base.BAR_MIN_Y * scale)
        s.BAR_MAX_Y = s.HEIGHT - s.BAR_HEIGHT - s.BAR_MIN_Y

    # fish
    s.FISH_SIZE = int(base.FISH_SIZE * scale)

    # track
    s.TRACK_X = int(base.TRACK_X * scale)
    s.TRACK_Y = int(base.TRACK_Y * scale)

    s.TRACK_WIDTH = int(base.TRACK_WIDTH * scale)
    s.TRACK_HEIGHT = int(base.TRACK_HEIGHT * scale)

    # progress bar
    s.PROGRESS_BAR_WIDTH = int(base.PROGRESS_BAR_WIDTH * scale)
    s.PROGRESS_BAR_HEIGHT = int(base.PROGRESS_BAR_HEIGHT * scale)

    if use_default == "horizontal":
        s.PROGRESS_BAR_Y = int(base.PROGRESS_BAR_Y * scale)
    else:
        s.PROGRESS_BAR_X = int(base.PROGRESS_BAR_X * scale)
        s.PROGRESS_BAR_Y = int(base.PROGRESS_BAR_Y * scale)

    # logic
    s.FPS = base.FPS
    s.BAR_MAX_SPEED = base.BAR_MAX_SPEED
    s.BAR_FRICTION = base.BAR_FRICTION
    s.BAR_FORCE_INC = base.BAR_FORCE_INC
    s.BAR_FORCE_DEC = base.BAR_FORCE_DEC
    s.BAR_FORCE_MAX = base.BAR_FORCE_MAX

    s.BAR_DRIFT = base.BAR_DRIFT_LEFT if use_default == "horizontal" else base.BAR_DRIFT_DOWN
    s.scale = scale
    
    return s

