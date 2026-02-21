# lobby.py
import os
import pygame

from gameData.config import BG_COLOR
from utils.gadgets import Button
from utils.load_img import load_ui_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


FONT_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)



def run_lobby(screen, S, FPS=60):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Fishing Lobby")
    clock = pygame.time.Clock()
    
    button_img = load_ui_image("button.png")
    bg_img = load_ui_image("lobby_bg.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))

    title_font = pygame.font.Font(FONT_PATH, int(42 * S.scale))
    btn_font = pygame.font.Font(FONT_PATH, int(24 * S.scale))

    # --- Buttons ---
    play_btn = Button(
        rect=(S.WIDTH//2 - 100 * S.scale, S.HEIGHT//2 - 160 * S.scale, 180 * S.scale, 95 * S.scale),
        text="PLAY",
        font=btn_font,
        image=button_img
    )

    rod_btn = Button(
        rect=(S.WIDTH//2 - 100 * S.scale, S.HEIGHT//2 - 70 * S.scale, 180 * S.scale, 95 * S.scale),
        text="ROD",
        font=btn_font,
        image=button_img
    )

    log_btn = Button(
        rect=(S.WIDTH//2 - 100 * S.scale, S.HEIGHT//2 + 20 * S.scale, 180 * S.scale, 95 * S.scale),
        text="BESTIARY",
        font=btn_font,
        image=button_img
    )

    settings_btn = Button(
        rect=(S.WIDTH//2 - 100 * S.scale, S.HEIGHT//2 + 110 * S.scale, 180 * S.scale, 95 * S.scale),
        text="SETTINGS",
        font=btn_font,
        image=button_img
    )

    quit_btn = Button(
        rect=(S.WIDTH//2 - 100 * S.scale, S.HEIGHT//2 + 200 * S.scale, 180 * S.scale, 95 * S.scale),
        text="QUIT",
        font=btn_font,
        image=button_img
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if play_btn.clicked(event):
                return "GAME"

            if rod_btn.clicked(event):
                return "SELECT_ROD"

            if log_btn.clicked(event):
                return "FISH_LOG"
            
            if settings_btn.clicked(event):
                return "SETTINGS"

            if quit_btn.clicked(event):
                return "QUIT"

        screen.blit(bg_img, (0, 0))

        # --- Title ---
        title = title_font.render("Fishing DDA", True, (51,25,0))
        screen.blit(title, title.get_rect(center=(S.WIDTH//2, S.HEIGHT//2 - 210 * S.scale)))

        # --- Draw Buttons ---
        play_btn.draw(screen)
        rod_btn.draw(screen)
        log_btn.draw(screen)
        settings_btn.draw(screen)
        quit_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
