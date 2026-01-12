# game.py
import pygame
import math
import random
import time

from config import *
from dda import update_fish_speed
import get_info


def run_game(logger):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DDA Experiment")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
        
    bar_x = WIDTH // 2 - BAR_WIDTH // 2
    bar_y = TRACK_Y

    encounter_start_time = time.time()

    fish_speed = 1.0
    progress = 0

    
    # random fish movement
    fish_x = WIDTH // 2
    fish_direction = random.choice([-1, 1])
    fish_speed = random.uniform(FISH_MIN_SPEED, FISH_MAX_SPEED)

    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
    fish_target_x = fish_x + fish_direction * distance
    fish_target_x = max(
        BAR_MIN_X,
        min(BAR_MAX_X + BAR_WIDTH - FISH_SIZE, fish_target_x)
    )

    fish_waiting = False
    resilient_timer = 0.0

    bar_velocity = 0.0
    bar_force = 0.0    # force cummulative

    # bouncing
    bar_bounced_left = False
    bar_bounced_right = False

    BAR_BOUNCE_DAMP = 0.5   

    fish_encounter = get_info.get_fish("Mythical")
    print(fish_encounter)

    success = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # set time
        current_time = time.time()
        freeze_active = (current_time - encounter_start_time) < ENCOUNTER_FREEZE_TIME

        # --- Progress animation during freeze ---
        if freeze_active and progress < PROGRESS_INIT:
            progress += PROGRESS_FILL_ANIM_SPEED
            progress = min(progress, PROGRESS_INIT)


        # --- Player Control ---
        if not freeze_active:
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

            elif bar_x >= WIDTH - BAR_WIDTH:
                bar_x = WIDTH - BAR_WIDTH
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
                if resilient_timer >= fish_encounter["FISH_RESILIENCE"]:
                    resilient_timer = 0
                    fish_waiting = False

                    fish_direction = random.choice([-1, 1])
                    fish_speed = random.uniform(FISH_MIN_SPEED+(fish_encounter["FISH_RESILIENCE"]*-1), FISH_MAX_SPEED+(fish_encounter["FISH_RESILIENCE"]*-1))

                    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
                    fish_target_x = fish_x + fish_direction * distance
                    fish_target_x = max(
                        BAR_MIN_X,
                        min(BAR_MAX_X + BAR_WIDTH - FISH_SIZE, fish_target_x)
                    )

            else:
                fish_x += fish_direction * fish_speed

                reached = (
                    (fish_direction == 1 and fish_x >= fish_target_x) or
                    (fish_direction == -1 and fish_x <= fish_target_x)
                )

                if reached:
                    fish_x = fish_target_x
                    fish_waiting = True


        # --- Collision (X-axis) ---
        fish_center = fish_x + FISH_SIZE / 2
        is_catching = bar_x < fish_center < bar_x + BAR_WIDTH
        # --- Progression Bar Logic ---
        if not freeze_active:
            if is_catching:
                progress += PROGRESS_UP_RATE + (fish_encounter["PROGRESS_SPD"]*PROGRESS_UP_RATE)
            else:
                progress -= PROGRESS_DOWN_RATE
        
        # clamp
        progress = max(0.0, min(1.0, progress))

        if progress >= 1.0:
            running = False
            success = True
        elif progress <= 0:
            running = False
        

        # --- DDA ---
        fish_speed = update_fish_speed(is_catching, fish_speed)

        # --- Log ---
        logger.log(BAR_WIDTH, fish_speed, is_catching)

        # --- Render ---
        screen.fill(BG_COLOR)
        # Background Track (Boundary)
        pygame.draw.rect(
            screen,
            TRACK_COLOR,
            (0, TRACK_Y, WIDTH, TRACK_HEIGHT)
        )

        pygame.draw.rect(screen, BAR_COLOR, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, FISH_COLOR, (fish_x, bar_y + 15, FISH_SIZE, FISH_SIZE))
        # --- Progress Bar Background ---
        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (
                WIDTH // 2 - PROGRESS_BAR_WIDTH // 2,
                PROGRESS_BAR_Y,
                PROGRESS_BAR_WIDTH,
                PROGRESS_BAR_HEIGHT
            )
        )

        # --- Progress Fill ---
        pygame.draw.rect(
            screen,
            (255, 215, 0),
            (
                WIDTH // 2 - PROGRESS_BAR_WIDTH // 2,
                PROGRESS_BAR_Y,
                int(PROGRESS_BAR_WIDTH * progress),
                PROGRESS_BAR_HEIGHT
            )
        )

        if fish_encounter["PROGRESS_SPD"] != 0:
            color = (0, 255, 0) if fish_encounter["PROGRESS_SPD"] > 0 else (255, 80, 80)

            text_surface = font.render(
                f"Progression Speed {fish_encounter["PROGRESS_SPD"]*100:+.0f}%",
                True,
                color
            )

            text_rect = text_surface.get_rect(
                center=(
                    WIDTH // 2,
                    PROGRESS_BAR_Y + PROGRESS_BAR_HEIGHT + 15
                )
            )

            screen.blit(text_surface, text_rect)

        screen.blit(font.render(
            f"Speed: {fish_speed:.2f} | Catching: {is_catching}",
            True, (200, 200, 200)), (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    return success

