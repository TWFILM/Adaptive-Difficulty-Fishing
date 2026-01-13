import pygame
import gameData.config


class ScaledConfig:
    pass


def build_scaled_config():
    info = pygame.display.Info()

    scale = min(
        info.current_w / gameData.config.WIDTH,
        info.current_h / gameData.config.HEIGHT
    )

    s = ScaledConfig()
    s.scale = scale

    # screen
    s.WIDTH = int(gameData.config.WIDTH * scale)
    s.HEIGHT = int(gameData.config.HEIGHT * scale)

    # bar
    s.BAR_WIDTH = int(gameData.config.BAR_WIDTH * scale)
    s.BAR_HEIGHT = int(gameData.config.BAR_HEIGHT * scale)
    s.BAR_MIN_X = int(gameData.config.BAR_MIN_X * scale)
    s.BAR_MAX_X = s.WIDTH - s.BAR_WIDTH - s.BAR_MIN_X

    # fish
    s.FISH_SIZE = int(gameData.config.FISH_SIZE * scale)

    # track
    s.TRACK_HEIGHT = int(gameData.config.TRACK_HEIGHT * scale)
    s.TRACK_Y = int(gameData.config.TRACK_Y * scale)

    # progress bar
    s.PROGRESS_BAR_WIDTH = int(gameData.config.PROGRESS_BAR_WIDTH * scale)
    s.PROGRESS_BAR_HEIGHT = int(gameData.config.PROGRESS_BAR_HEIGHT * scale)
    s.PROGRESS_BAR_Y = int(gameData.config.PROGRESS_BAR_Y * scale)

    # logic (no change)
    s.FPS = gameData.config.FPS
    s.BAR_MAX_SPEED = gameData.config.BAR_MAX_SPEED
    s.BAR_FRICTION = gameData.config.BAR_FRICTION
    s.BAR_FORCE_INC = gameData.config.BAR_FORCE_INC
    s.BAR_FORCE_DEC = gameData.config.BAR_FORCE_DEC
    s.BAR_FORCE_MAX = gameData.config.BAR_FORCE_MAX
    s.BAR_DRIFT_LEFT = gameData.config.BAR_DRIFT_LEFT

    return s
