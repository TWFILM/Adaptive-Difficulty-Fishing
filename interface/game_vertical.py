# game_vertical.py
import pygame
import random
import time
import os

from gameData.config_vertical import *
from dda import update_fish_speed
from gameData.get_info import get_fish, get_fishing_rod_info, get_random_rarity
from utils.load_img import run_end_screen_meme


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH = os.path.join(
    ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf"
)


def run_game_vertical(screen, S, logger, rod_name):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("DDA Experiment (Vertical)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, int(18 * S.scale))

    # ── ROD ─────────────────────────
    rod_using = get_fishing_rod_info(rod_name)

    player_bar_height = S.BAR_HEIGHT + (rod_using["CONTROLLED"] * S.BAR_HEIGHT)
    bar_y = S.TRACK_Y + S.TRACK_HEIGHT // 2 - player_bar_height // 2
    bar_x = S.TRACK_X

    encounter_start_time = time.time()

    # ── PROGRESS ─────────────────────
    progress = 0
    progress_color = PROGRESS_BAR_COLOR
    progress_addition = 0

    if rod_using["name"] == "Rod of the Conqueror":
        progress_addition = 0.26
        progress_color = (255, 215, 0)

    # ── FISH ─────────────────────────
    fish_y = S.TRACK_Y + S.TRACK_HEIGHT // 2 - S.FISH_SIZE // 2
    fish_direction = random.choice([-1, 1])
    fish_speed = random.uniform(FISH_MIN_SPEED, FISH_MAX_SPEED)

    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
    fish_target_y = fish_y + fish_direction * distance
    fish_target_y = max(
            S.BAR_MIN_Y + (S.FISH_SIZE+10),
            min(S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10), fish_target_y)
        )

    fish_waiting = False
    resilient_timer = 0.0

    # ── PLAYER PHYSICS ───────────────
    bar_velocity = 0.0
    bar_force = 0.0

    bar_bounced_top = False
    bar_bounced_bottom = False
    BAR_BOUNCE_DAMP = 0.5

    # ── FISH DATA ────────────────────
    fish_encounter = get_fish(get_random_rarity(rod_using["name"]))
    fish_resilience = fish_encounter["FISH_RESILIENCE"] + rod_using["RESILIENCE"]
    fish_progress = fish_encounter["PROGRESS_SPD"] + rod_using["PROGRESS_SPD"]

    if rod_using["name"] == "Meme Rod":
        fish_progress = -0.9

    success = [False, None, None]
    running = True

    # ─────────────────────────────────
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.time()
        freeze_active = (current_time - encounter_start_time) < ENCOUNTER_FREEZE_TIME

        # ── Freeze Progress Fill ──────
        if freeze_active and progress < (PROGRESS_INIT + progress_addition):
            progress += PROGRESS_FILL_ANIM_SPEED
            progress = min(progress, PROGRESS_INIT + progress_addition)

        # ── PLAYER CONTROL ────────────
        if not freeze_active:
            mouse_pressed = pygame.mouse.get_pressed()[0]

            if mouse_pressed:
                bar_force += BAR_FORCE_INC
            else:
                bar_force -= BAR_FORCE_DEC

            bar_force = max(0.0, min(BAR_FORCE_MAX, bar_force))

            bar_accel = BAR_DRIFT_DOWN - bar_force
            bar_velocity += bar_accel
            bar_velocity *= BAR_FRICTION
            bar_velocity = max(-BAR_MAX_SPEED, min(BAR_MAX_SPEED, bar_velocity))

            bar_y += bar_velocity

            # bounce
            if bar_y <= S.BAR_MIN_Y :
                bar_y = S.BAR_MIN_Y
                if not bar_bounced_top:
                    bar_velocity = -bar_velocity * BAR_BOUNCE_DAMP
                    bar_bounced_top = True
                else:
                    bar_velocity = max(bar_velocity, 0)

            elif bar_y + player_bar_height >= S.BAR_MAX_Y + S.BAR_HEIGHT:
                bar_y = S.BAR_MAX_Y + S.BAR_HEIGHT - player_bar_height
                if not bar_bounced_bottom:
                    bar_velocity = -bar_velocity * BAR_BOUNCE_DAMP
                    bar_bounced_bottom = True
                else:
                    bar_velocity = min(bar_velocity, 0)

            else:
                bar_bounced_top = False
                bar_bounced_bottom = False

        # ── Fish Movement (Vertical, same like horizontal) ──
        if not freeze_active:
            if fish_waiting:
                resilient_timer += clock.get_time() / 1000
                if resilient_timer >= fish_resilience:
                    resilient_timer = 0
                    fish_waiting = False

                    fish_direction = random.choice([-1, 1])
                    fish_speed = random.uniform(
                        FISH_MIN_SPEED + (fish_resilience * -1),
                        FISH_MAX_SPEED + (fish_resilience * -1)
                    )

                    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)

                    fish_target_y = fish_y + fish_direction * distance
                    fish_target_y = max(
                        S.BAR_MIN_Y + (S.FISH_SIZE+10),
                        min(S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10), fish_target_y)
                    )

            else:
                fish_y += fish_direction * fish_speed

                # reach target
                if ((fish_direction == 1 and fish_y >= fish_target_y) or
                    (fish_direction == -1 and fish_y <= fish_target_y)):
                    fish_y = fish_target_y
                    fish_waiting = True

                # hard boundary
                if fish_y <= S.BAR_MIN_Y + (S.FISH_SIZE+10):
                    fish_y = S.BAR_MIN_Y + (S.FISH_SIZE+10)
                    fish_direction = 1
                    fish_waiting = True

                elif fish_y >= S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10):
                    fish_y = S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10)
                    fish_direction = -1
                    fish_waiting = True


        # ── COLLISION ─────────────────
        fish_center = fish_y + S.FISH_SIZE / 2
        is_catching = bar_y <= fish_center <= bar_y + player_bar_height

        if not freeze_active:
            if is_catching:
                progress += PROGRESS_UP_RATE + (fish_progress * PROGRESS_UP_RATE)
            else:
                progress -= PROGRESS_DOWN_RATE

        progress = max(0.0, min(1.0, progress))

        if progress >= 1.0:
            running = False
            success = [True, fish_encounter["rarity"], fish_encounter["name"]]
        elif progress <= 0:
            running = False

        fish_speed = update_fish_speed(is_catching, fish_speed)
        logger.log(player_bar_height, fish_speed, is_catching)

        # ── RENDER ────────────────────
        screen.fill(BG_COLOR)

        pygame.draw.rect(
            screen, TRACK_COLOR,
            (S.TRACK_X, S.TRACK_Y, S.TRACK_WIDTH, S.TRACK_HEIGHT)
        )

        pygame.draw.rect(
            screen, BAR_COLOR,
            (bar_x, bar_y, S.BAR_WIDTH, player_bar_height)
        )

        pygame.draw.rect(
            screen, FISH_COLOR,
            (bar_x + (S.BAR_WIDTH // 2 - S.FISH_SIZE // 2), fish_y,
             S.FISH_SIZE, S.FISH_SIZE)
        )

        pygame.draw.rect(
            screen, (80, 80, 80),
            (S.PROGRESS_BAR_X, S.PROGRESS_BAR_Y,
             S.PROGRESS_BAR_WIDTH, S.PROGRESS_BAR_HEIGHT)
        )

        pygame.draw.rect(
            screen, progress_color,
            (S.PROGRESS_BAR_X,
             S.PROGRESS_BAR_Y + S.PROGRESS_BAR_HEIGHT * (1 - progress),
             S.PROGRESS_BAR_WIDTH,
             S.PROGRESS_BAR_HEIGHT * progress)
        )

        if fish_progress != 0:
            color = (0, 255, 0) if fish_progress > 0 else (255, 80, 80)

            text_surface = font.render(
                f"Progression Speed {(fish_progress)*100:+.0f}%",
                True,
                color
            )

            text_rect = text_surface.get_rect(
                center=(
                    S.WIDTH // 2,
                    S.PROGRESS_BAR_Y + S.PROGRESS_BAR_HEIGHT + 15
                )
            )

            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    logger.export()

    if rod_using["name"] == "Meme Rod" and success[0]:
        run_end_screen_meme(screen, clock, duration=4)

    pygame.quit()
    return success
