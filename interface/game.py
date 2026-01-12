# game.py
import pygame
import math
import random
import time
import os

from gameData.config import *
from dda import update_fish_speed
from gameData.get_info import get_fish, get_fishing_rod_info, get_random_rarity
from gameData.load_img import run_end_screen_meme

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH1 = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)

def run_game(screen, S, logger, rod_name):
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DDA Experiment")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH1, 18)

    # RODDD
    rod_using = get_fishing_rod_info(rod_name)

    player_bar_width = S.BAR_WIDTH+(rod_using["CONTROLLED"]*S.BAR_WIDTH)   # player control bar    
    bar_x = S.WIDTH // 2 - player_bar_width // 2
    bar_y = S.TRACK_Y
    
    encounter_start_time = time.time()

    fish_speed = 1.0
    progress = 0
    progress_bar_color = PROGRESS_BAR_COLOR
    # for Rod of the Conqueror
    progress_addition = 0
    if rod_using["name"] == "Rod of the Conqueror":
        progress_addition = 0.21
        progress_bar_color = (255, 215, 0)
    
    # random fish movement
    fish_x = ( S.WIDTH // 2 ) - (S.FISH_SIZE // 2)
    fish_direction = random.choice([-1, 1])
    fish_speed = random.uniform(FISH_MIN_SPEED, FISH_MAX_SPEED)

    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
    fish_target_x = fish_x + fish_direction * distance
    fish_target_x = max(
        S.BAR_MIN_X,
        min(S.BAR_MAX_X + S.BAR_WIDTH - S.FISH_SIZE, fish_target_x)
    )

    fish_waiting = False
    resilient_timer = 0.0

    bar_velocity = 0.0
    bar_force = 0.0    # force cummulative

    # bouncing
    bar_bounced_left = False
    bar_bounced_right = False

    BAR_BOUNCE_DAMP = 0.5   
    
    # the fish you are catching
    fish_encounter = get_fish(get_random_rarity(rod_using["name"]))
    # print(fish_encounter)

    fish_resilience = fish_encounter["FISH_RESILIENCE"]+rod_using["RESILIENCE"]
    fish_progress = fish_encounter["PROGRESS_SPD"]+rod_using["PROGRESS_SPD"]
    if rod_using["name"] == "Meme Rod":
        fish_progress = -0.95

    success = [False, "None", "None"]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # set time
        current_time = time.time()
        freeze_active = (current_time - encounter_start_time) < ENCOUNTER_FREEZE_TIME

        # --- Progress animation during freeze ---
        if freeze_active and progress < (PROGRESS_INIT + progress_addition):
            progress += PROGRESS_FILL_ANIM_SPEED
            progress = min(progress, PROGRESS_INIT+progress_addition)


        # --- Player Control ---
        if not freeze_active:
            # Meme Rod's Secret Passive
            progress_bar_color = PROGRESS_BAR_COLOR 
            if rod_using["name"] == "Meme Rod" and player_bar_width <= 600 and fish_encounter["name"] != "Meme Fish":
                player_bar_width += 0.1

            if fish_encounter["name"] == "Meme Fish" and player_bar_width >= 0:
                player_bar_width -= 0.25

            mouse_pressed = pygame.mouse.get_pressed()[0]

            if mouse_pressed:
                # continue increasing when you clicked mouse
                bar_force += BAR_FORCE_INC
            else:
                # decrease force that drags player bar to the left
                bar_force -= BAR_FORCE_DEC

            # clamp
            bar_force = max(0.0, min(BAR_FORCE_MAX, bar_force))

            # physics force
            bar_acceleration = BAR_DRIFT_LEFT + bar_force

            # update velocity
            bar_velocity += bar_acceleration

            # friction
            bar_velocity *= BAR_FRICTION

            # speed limit
            bar_velocity = max(-BAR_MAX_SPEED, min(BAR_MAX_SPEED, bar_velocity))

            # update position
            bar_x += bar_velocity


            # update position
            # ---- Edge Collision with Single Bounce ----
            if bar_x <= 0:
                bar_x = 0
                if not bar_bounced_left:
                    bar_velocity = -bar_velocity * BAR_BOUNCE_DAMP
                    bar_bounced_left = True
                else:
                    bar_velocity = max(bar_velocity, 0)

            elif bar_x >= S.WIDTH - player_bar_width:
                bar_x = S.WIDTH - player_bar_width
                if not bar_bounced_right:
                    bar_velocity = -bar_velocity * BAR_BOUNCE_DAMP
                    bar_bounced_right = True
                else:
                    bar_velocity = min(bar_velocity, 0)
            else:
                # reset flags when bar leaves edge
                bar_bounced_left = False
                bar_bounced_right = False


        # --- Fish Random Movement with Resilience ---
        # Fish Movement
        if not freeze_active:
            if fish_waiting:
                resilient_timer += clock.get_time() / 1000
                if resilient_timer >= fish_resilience:
                    resilient_timer = 0
                    fish_waiting = False

                    fish_direction = random.choice([-1, 1])
                    fish_speed = random.uniform(FISH_MIN_SPEED+(fish_resilience*-1), FISH_MAX_SPEED+(fish_resilience*-1))

                    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
                    fish_target_x = fish_x + fish_direction * distance
                    fish_target_x = max(
                        S.BAR_MIN_X,
                        min(S.BAR_MAX_X + S.BAR_WIDTH - S.FISH_SIZE, fish_target_x)
                    )

            else:
                fish_x += fish_direction * fish_speed

                # check reach target
                if ((fish_direction == 1 and fish_x >= fish_target_x) or
                    (fish_direction == -1 and fish_x <= fish_target_x)
                    ):
                    fish_x = fish_target_x
                    fish_waiting = True

                # hard boundary
                if fish_x <= S.BAR_MIN_X:
                    fish_x = S.BAR_MIN_X
                    fish_direction = 1
                    fish_waiting = True

                elif fish_x >= S.BAR_MAX_X + S.BAR_WIDTH - S.FISH_SIZE :
                    fish_x = S.BAR_MAX_X + S.BAR_WIDTH - S.FISH_SIZE
                    fish_direction = -1
                    fish_waiting = True


        # --- Collision (X-axis) ---
        fish_center = fish_x + S.FISH_SIZE / 2
        is_catching = bar_x <= fish_center <= bar_x + player_bar_width
        # --- Progression Bar Logic ---
        if not freeze_active:
            if is_catching:
                progress += PROGRESS_UP_RATE + ((fish_progress)*PROGRESS_UP_RATE)
            else:
                progress -= PROGRESS_DOWN_RATE
        
        # clamp
        progress = max(0.0, min(1.0, progress))

        if progress >= 1.0:
            running = False
            success[0] = True
            success[1] = fish_encounter["rarity"]
            success[2] = fish_encounter["name"]
        elif progress <= 0:
            running = False
        

        # --- DDA ---
        fish_speed = update_fish_speed(is_catching, fish_speed)

        # --- Log ---
        logger.log(player_bar_width, fish_speed, is_catching)

        # --- Render ---
        screen.fill(BG_COLOR)
        # Background Track (Boundary)
        pygame.draw.rect(
            screen,
            TRACK_COLOR,
            (0, S.TRACK_Y, S.WIDTH, S.TRACK_HEIGHT)
        )

        pygame.draw.rect(screen, BAR_COLOR, (bar_x, bar_y, player_bar_width, S.BAR_HEIGHT))
        pygame.draw.rect(screen, FISH_COLOR, (fish_x, bar_y + 15, S.FISH_SIZE, S.FISH_SIZE))
        # --- Progress Bar Background ---
        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (
                S.WIDTH // 2 - S.PROGRESS_BAR_WIDTH // 2,
                S.PROGRESS_BAR_Y,
                S.PROGRESS_BAR_WIDTH,
                S.PROGRESS_BAR_HEIGHT
            )
        )

        # --- Progress Fill ---
        pygame.draw.rect(
            screen,
            progress_bar_color,
            (
                S.WIDTH // 2 - S.PROGRESS_BAR_WIDTH // 2,
                S.PROGRESS_BAR_Y,
                int(S.PROGRESS_BAR_WIDTH * progress),
                S.PROGRESS_BAR_HEIGHT
            )
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

        screen.blit(font.render(
            f"Speed: {fish_speed:.2f} | Catching: {is_catching}",
            True, (200, 200, 200)), (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    logger.export()

    # Meme Rod only!
    if rod_using["name"] == "Meme Rod" and success[0] is True:
        run_end_screen_meme(screen, clock, duration=4)

    pygame.quit()
    return success

