import pygame
import os
from utils.gadgets import Button, Switch
from gameData.config import BG_COLOR, FPS
from utils.save_writer import SaveManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FONT_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf")


def run_settings(screen, S, settings_data):

    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()

    font_title = pygame.font.Font(FONT_PATH, int(48 * S.scale))
    font_label = pygame.font.Font(FONT_PATH, int(20 * S.scale))
    gameplay_label = pygame.font.Font(FONT_PATH, int(14 * S.scale))
    font_btn = pygame.font.Font(FONT_PATH, int(24 * S.scale))

    CENTER_X = S.WIDTH // 2
    ROW_Y_START = S.HEIGHT * 0.2
    ROW_GAP = 70 * S.scale

    LABEL_X = CENTER_X - 240 * S.scale
    CONTROL_X = CENTER_X + 20 * S.scale

    CONTROL_W = 260 * S.scale
    CONTROL_H = 45 * S.scale

    # ──────────────────────────────
    # Resolution Options
    # ──────────────────────────────

    resolutions = [
        (600, 800),
        (700, 900),
        (800, 1000),
        (900, 1100),
        (1000, 1200)
    ]

    res_index = resolutions.index(
        (settings_data["width"], settings_data["height"])
    )

    resolution_btn = Button(
        rect=(CONTROL_X*0.9, ROW_Y_START, CONTROL_W, CONTROL_H),
        text=f"{resolutions[res_index][0]} x {resolutions[res_index][1]}",
        font=font_btn
    )

    # Gameplay
    gameplay_switch = Switch(
        rect=(CONTROL_X*0.9, ROW_Y_START + ROW_GAP, CONTROL_W, CONTROL_H),
        left_text="HORIZONTAL",
        right_text="VERTICAL",
        font=gameplay_label,
        initial=settings_data["gameplay"] == "horizontal"
    )

    # SFX
    sfx_switch = Switch(
        rect=(CONTROL_X*0.9, ROW_Y_START + ROW_GAP * 2, CONTROL_W, CONTROL_H),
        left_text="ON",
        right_text="MUTE",
        font=font_btn,
        initial=settings_data["sfx"]
    )

    # Mode
    modes = ["Default", "EASY", "HARD",  "DDA"]
    mode_index = modes.index(settings_data["mode"])

    mode_btn = Button(
        rect=(CONTROL_X*0.9, ROW_Y_START + ROW_GAP * 3, CONTROL_W, CONTROL_H),
        text=settings_data["mode"],
        font=font_btn
    )

    # ──────────────────────────────
    # Extra Navigation Buttons
    # ──────────────────────────────

    howto_btn = Button(
        rect=(S.WIDTH * 0.05,
              ROW_Y_START + ROW_GAP * 4,
              S.WIDTH * 0.9,
              45 * S.scale),
        text="HOW TO PLAY",
        font=font_btn
    )

    credits_btn = Button(
        rect=(S.WIDTH * 0.05,
              ROW_Y_START + ROW_GAP * 4.8,
              S.WIDTH * 0.9,
              45 * S.scale),
        text="CREDITS",
        font=font_btn
    )

    delete_btn = Button(
        rect=(S.WIDTH * 0.05,
            ROW_Y_START + ROW_GAP * 5.6,
            S.WIDTH * 0.9,
            45 * S.scale),
        text="DELETE GAME DATA",
        font=font_btn
    )

    cancel_btn = Button(
        rect=(S.WIDTH * 0.05,
            ROW_Y_START + ROW_GAP * 7,
            220 * S.scale,
            55 * S.scale),
        text="CANCEL",
        font=font_btn
    )

    back_btn = Button(
        rect=(S.WIDTH * 0.95 - 220 * S.scale,
            ROW_Y_START + ROW_GAP * 7,
            220 * S.scale,
            55 * S.scale),
        text="SAVE",
        font=font_btn
    )

    save = SaveManager()
    running = True
    confirm_delete = False

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "QUIT"

            # Resolution
            if resolution_btn.clicked(event):
                res_index = (res_index + 1) % len(resolutions)
                w, h = resolutions[res_index]
                settings_data["width"] = w
                settings_data["height"] = h
                resolution_btn.text = f"{w} x {h}"

            # Gameplay
            if gameplay_switch.clicked(event):
                settings_data["gameplay"] = (
                    "horizontal" if gameplay_switch.value else "vertical"
                )

            # SFX
            if sfx_switch.clicked(event):
                settings_data["sfx"] = sfx_switch.value

            # Mode
            if mode_btn.clicked(event):
                mode_index = (mode_index + 1) % len(modes)
                settings_data["mode"] = modes[mode_index]
                mode_btn.text = modes[mode_index]

            # Navigate
            if howto_btn.clicked(event):
                return "HOW_TO_PLAY"

            if credits_btn.clicked(event):
                return "CREDITS"
            
            # DELETE DATA
            if delete_btn.clicked(event):

                if not confirm_delete:
                    confirm_delete = True
                    delete_btn.text = "CLICK AGAIN TO CONFIRM"
                    delete_btn.bg_color = (200, 50, 50)
                    delete_btn.hover_color = (220, 50, 50)
                else:
                    # Reset Player Data
                    save.data["player"] = {
                        "rod": "Novice Rod",
                        "catched_fish": [],
                        "total_catched": 0,
                        "catched_streak": 0,
                        "perfect_catches": 0,
                        "unlocked_rods": ["Novice Rod"],
                        "shown_unlock_notice": ["Novice Rod"]
                    }

                    save.save()

                    confirm_delete = False
                    delete_btn.text = "DATA DELETED!"
                    delete_btn.bg_color = (70, 70, 70)
                    delete_btn.hover_color = (70, 70, 70)

            if cancel_btn.clicked(event):
                return "LOBBY"  


            # Back (Apply Resolution)
            if back_btn.clicked(event):

                save.data["settings_data"] = settings_data
                save.save()

                return "LOBBY"  

        # ──────────────────────────────
        # DRAW
        # ──────────────────────────────

        screen.fill(BG_COLOR)

        title = font_title.render("SETTINGS", True, (220, 220, 220))
        screen.blit(title, title.get_rect(center=(CENTER_X, S.HEIGHT * 0.12)))

        # Labels
        screen.blit(
            font_label.render("RESOLUTION", True, (200, 200, 200)),
            (LABEL_X, ROW_Y_START + 15 * S.scale)
        )

        screen.blit(
            font_label.render("GAMEPLAY", True, (200, 200, 200)),
            (LABEL_X, ROW_Y_START + ROW_GAP + 15 * S.scale)
        )

        screen.blit(
            font_label.render("SFX", True, (200, 200, 200)),
            (LABEL_X, ROW_Y_START + ROW_GAP * 2 + 15 * S.scale)
        )

        screen.blit(
            font_label.render("MODE", True, (200, 200, 200)),
            (LABEL_X, ROW_Y_START + ROW_GAP * 3 + 15 * S.scale)
        )

        # Draw Controls
        resolution_btn.draw(screen)
        gameplay_switch.draw(screen)
        sfx_switch.draw(screen)
        mode_btn.draw(screen)

        howto_btn.draw(screen)
        credits_btn.draw(screen)
        delete_btn.draw(screen)
        cancel_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
