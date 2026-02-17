# game_vertical.py
import pygame
import random
import time
import os

from gameData.config import *
from dda import DDAManager, update_fish_speed
from gameData.get_info import get_fish, get_fishing_rod_info, get_random_rarity
from utils.load_img import *
from utils.load_audio import trigger_jumpscare, play_stab_sfx, stop_meme_sfx
from utils.save_writer import SaveManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH = os.path.join(
    ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf"
)


def run_game_vertical(screen, S, logger, rod_name, difficulty_mode="DDA"):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(f"DDA Experiment - Mode: {difficulty_mode}") 
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, int(18 * S.scale))

    # LOAD SAVE DATA
    save = SaveManager()
    CATCHED_STREAK = save.data["player"]["catched_streak"]

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
    conqueror_active = False

    if rod_using["name"] == "Rod of the Conqueror":
        conqueror_active = True
        progress_addition = 0.26
        progress_color = (255, 215, 0)
        mult = 0.5
    
    if rod_using["name"] == "Anchor Rod":
        is_anchor_active = True
        player_bar_height_before = S.BAR_HEIGHT + (rod_using["CONTROLLED"] * S.BAR_HEIGHT)

    # ── FISH DATA ────────────────────
    fish_encounter = get_fish(get_random_rarity(rod_using["name"]))
    fish_resilience = fish_encounter["FISH_RESILIENCE"] + rod_using["RESILIENCE"]
    fish_progress = fish_encounter["PROGRESS_SPD"] + rod_using["PROGRESS_SPD"]

    # --- DDA MANAGER SETUP ---
    dda_manager = None
    if difficulty_mode == "DDA":
        dda_manager = DDAManager(fish_resilience=fish_resilience, fish_progress=fish_progress)
        # Use a neutral starting speed for DDA mode, the manager will adjust it
        fish_speed = 1.5
    else:
        # Fallback for non-DDA modes
        fish_speed = {"EASY": 1.0, "MEDIUM": 2.0, "HARD": 3.0}.get(difficulty_mode, 1.0)
    
    # ── FISH ─────────────────────────
    fish_y = S.TRACK_Y + S.TRACK_HEIGHT // 2 - S.FISH_SIZE // 2
    fish_direction = random.choice([-1, 1])

    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
    fish_target_y = fish_y + fish_direction * distance
    fish_target_y = max(
            S.BAR_MIN_Y + (S.FISH_SIZE+10),
            min(S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10), fish_target_y)
        )
    
    EXTRA_WIDTH = 10  
    fish_width = S.TRACK_WIDTH + EXTRA_WIDTH

    fish_x_draw = (
        bar_x
        + (S.BAR_WIDTH // 2 - fish_width // 2)
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
        choices = random.choices([1, 2, 3])
        if 1 in choices:
            fish_progress = -0.9  # Meme Rod special passive

    # for Shear Rod
    if rod_using["name"] == "Shear Rod":
        knife_fill_remaining = 0.0
        KNIFE_FILL_TOTAL = 0.05
        KNIFE_FILL_SPEED = 0.075   # stop fish movement for 0.75 sec
        knife_checked = False  
        # angle_mode = 1
        mult = 0.5

    knife_active = False
    
    is_perfect_catch = True
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
            if rod_using["name"] == "Rod of the Conqueror":
                progress_color = PROGRESS_BAR_COLOR 
                conqueror_active = False
            if rod_using["name"] == "Meme Rod" :
                if 1 in choices and player_bar_height <= S.TRACK_HEIGHT and fish_encounter["name"] != "Meme Fish":
                    player_bar_height += player_bar_height * 0.005
            if rod_using["name"] == "Anchor Rod" and is_anchor_active:
                if is_catching:
                    if player_bar_height > player_bar_height_before*0.3:
                        player_bar_height -= 0.25
                        fish_progress += 0.0003
                
                else:
                    is_anchor_active = False
                    fish_progress = fish_encounter["PROGRESS_SPD"]+rod_using["PROGRESS_SPD"]
                    player_bar_height = player_bar_height_before

            if fish_encounter["name"] == "Meme Fish" and player_bar_height >= 0 and rod_using["name"] != "Meme Rod":
                player_bar_height -= 0.25

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

        # ── Fish Movement (Vertical, DDA-enabled) ──
        if not freeze_active:
            if fish_waiting:
                resilient_timer += clock.get_time() / 1000

                # ===== Shear Rod logic =====
                if rod_using["name"] == "Shear Rod" and not knife_active and not knife_checked:
                    if random.random() < 0.25:
                        play_stab_sfx()
                        mult = 0.5
                        knife_active = True
                        knife_checked = True
                        knife_fill_remaining = KNIFE_FILL_TOTAL
                        resilient_timer = 0
                        fish_waiting = True

                # In DDA mode, get resilience from the manager, otherwise use the static value
                current_resilience = dda_manager.get_modified_resilience() if dda_manager else fish_resilience

                if resilient_timer >= current_resilience:
                    resilient_timer = 0
                    fish_waiting = False
                    fish_direction = random.choice([-1, 1])

                    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
                    fish_target_y = fish_y + fish_direction * distance
                    fish_target_y = max(
                        S.BAR_MIN_Y + (S.FISH_SIZE+10),
                        min(S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10), fish_target_y)
                    )
            else:
                # >>>>>>>>>>>> CHAOS LOGIC START <<<<<<<<<<<<
                if difficulty_mode in ["DDA", "HARD", "MEDIUM"]:
                    if dda_manager:
                        chaos_chance = dda_manager.get_chaos_chance()
                    else: # Fallback to original logic for non-DDA modes
                        chaos_chance = 0.02 if difficulty_mode == "HARD" else 0.01
                    
                    if random.random() < chaos_chance:
                        # 40% chance to stop, 60% chance to juke
                        if random.random() < 0.4: 
                            fish_waiting = True
                            resilient_timer = 0 
                        else: # Juke!
                            fish_direction *= -1
                            distance = random.randint(50, 150) # Short, sharp movement
                            fish_target_y = fish_y + fish_direction * distance
                            fish_target_y = max(S.BAR_MIN_Y + (S.FISH_SIZE+10), min(S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10), fish_target_y))
                            # Small speed burst on juke
                            fish_speed = min(3.5, fish_speed * 1.3)
                # >>>>>>>>>>>> CHAOS LOGIC END <<<<<<<<<<<<
                
                fish_y += fish_direction * fish_speed
                if rod_name == "Meme Rod" and 2 in choices:
                        fish_x_draw += fish_direction * fish_speed
                        S.TRACK_Y += fish_direction * fish_speed
                        S.TRACK_X += fish_direction * fish_speed
                        bar_x += fish_direction * fish_speed

                # reach target
                if ((fish_direction == 1 and fish_y >= fish_target_y) or
                    (fish_direction == -1 and fish_y <= fish_target_y)):
                    fish_y = fish_target_y
                    fish_waiting = True
                    knife_checked = False

                # hard boundary
                if fish_y <= S.BAR_MIN_Y + (S.FISH_SIZE+10):
                    fish_y = S.BAR_MIN_Y + (S.FISH_SIZE+10)
                    fish_direction = 1
                    fish_waiting = True
                    knife_checked = False

                elif fish_y >= S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10):
                    fish_y = S.BAR_MAX_Y + S.BAR_HEIGHT - (S.FISH_SIZE+10)
                    fish_direction = -1
                    fish_waiting = True
                    knife_checked = False


        # ── COLLISION ─────────────────
        fish_center = fish_y + S.FISH_SIZE / 2
        is_catching = bar_y <= fish_center <= bar_y + player_bar_height

        # --- Shear Rod fill animation ---
        if knife_active:
            progress_color = (255, 215, 0)

            k_dt = clock.get_time() / 1000
            fill_amount = KNIFE_FILL_SPEED * k_dt

            actual_fill = min(fill_amount, knife_fill_remaining)
            knife_fill_remaining -= actual_fill
            progress += actual_fill
                    
            if knife_fill_remaining <= 0:
                knife_active = False
                progress_color = PROGRESS_BAR_COLOR

        # --- Progression Logic (DDA-enabled) ---
        if not freeze_active:
            if is_catching:
                # Use DDA-modified progress rate if available
                current_fish_progress = dda_manager.get_modified_progress() if dda_manager else fish_progress
                base_gain = PROGRESS_UP_RATE * (1.0 + current_fish_progress)
                actual_gain = max(PROGRESS_UP_RATE * 0.1, base_gain) # Min gain guarantee
                progress += actual_gain
            else:
                progress -= PROGRESS_DOWN_RATE
                is_perfect_catch = False
                actual_gain = -PROGRESS_DOWN_RATE
        
        progress = max(0.0, min(1.0, progress))

        if progress >= 1.0:
            running = False
            success = [True, fish_encounter["rarity"], fish_encounter["name"]]
        elif progress <= 0:
            running = False

        # --- DDA UPDATES ---
        if dda_manager:
            dda_manager.update(is_catching)
            fish_speed = dda_manager.adjust_fish_speed(fish_speed, is_catching)
        else:
            # Legacy speed update for non-DDA modes
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
            screen,
            FISH_COLOR,
            (fish_x_draw, fish_y, fish_width, S.FISH_SIZE), border_radius=3
        )

        if rod_using["name"] == "Prismatic Rod":
            if pygame.time.get_ticks() % 1000 < 800 :
                pygame.draw.rect(screen, (255, 255, 255), (bar_x + (S.BAR_WIDTH // 2 - S.FISH_SIZE // 2), fish_target_y, S.FISH_SIZE, S.FISH_SIZE))

        if knife_active or conqueror_active:
            if conqueror_active:
                mult += 0.1
                knife_length = int(S.WIDTH*2)
                knife_thickness = int(S.FISH_SIZE * (mult))
                angle = 0 
            else:
                mult += 0.1
                knife_length = int(S.HEIGHT*(2-mult if (2-mult)>=0 else 0))
                knife_thickness = int(S.FISH_SIZE//mult)
                angle = 0
                # knife_length = int(S.FISH_SIZE * 2.5)
                # knife_thickness = int(3 * S.scale)
                # angle = random.choice([15, 30, 60])*angle_mode # for random / \ |

            knife_surf = pygame.Surface(
                (knife_length, knife_thickness),
                pygame.SRCALPHA
            )
            knife_surf.fill(progress_color)

            knife_rotated = pygame.transform.rotate(knife_surf, angle)
           
            fish_x = bar_x + (S.BAR_WIDTH // 2 - S.FISH_SIZE // 2)
            fish_center_x = fish_x + (S.FISH_SIZE // 2)
            fish_center_y = fish_y + (S.FISH_SIZE // 2)

            knife_rect = knife_rotated.get_rect(
                center=(fish_center_x, fish_center_y)
            )

            screen.blit(knife_rotated, knife_rect)

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
                    S.TRACK_HEIGHT + S.TRACK_Y + 18 * S.scale
                )
            )

            screen.blit(text_surface, text_rect)

        screen.blit(font.render(
            f"Speed: {fish_speed:.2f} | Catching: {is_catching} | Catched Streak: {CATCHED_STREAK}",
            True, (200, 200, 200)), (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    logger.export()
    if success[0]:
        screen.blit(font.render(
            f"You caught the {fish_encounter['rarity']} {fish_encounter['name']}!",
            True, (200, 200, 200)), ((S.WIDTH // 2 ) - (font.size(f"You caught the {fish_encounter['rarity']} {fish_encounter['name']}!")[0] // 2), S.HEIGHT * 0.09))
        
        if not fish_encounter["name"] in save.data["player"]["catched_fish"]:
            save.data["player"]["catched_fish"].append(fish_encounter["name"])
            
        save.data["player"]["total_catched"] += 1
        save.data["player"]["catched_streak"] += 1
        if is_perfect_catch:
            save.data["player"]["perfect_catches"] += 1
        save.save()
        pygame.display.flip()
        time.sleep(3)
    else:
        fail_message = "The fish got away..."
        text_surface = font.render(fail_message, True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=(S.WIDTH // 2, S.HEIGHT * 0.1))
        screen.blit(text_surface, text_rect)

        save.data["player"]["catched_streak"] = 0
        save.save()
        pygame.display.flip()
        time.sleep(3)

    if rod_using["name"] == "Meme Rod" and success[0] is True and 3 in choices:
        stop_meme_sfx()
        trigger_jumpscare(meme_fish=False)
        run_end_screen_meme(screen, clock, duration=4, meme_fish=False)
    
    if fish_encounter["name"] == "Meme Fish" and success[0] is False:
        trigger_jumpscare(meme_fish=True)
        run_end_screen_meme(screen, clock, duration=4, meme_fish=True)

    pygame.quit()
    return success
