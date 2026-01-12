# lobby.py
import os
import pygame

from gameData.config import BG_COLOR, FPS
from interface.gadgets import Button

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH1 = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "Underlines-PVjX2.ttf"
)

FONT_PATH2 = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)

def run_lobby(screen, S):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Fishing Lobby")
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(FONT_PATH1, 42)
    btn_font = pygame.font.Font(FONT_PATH2, 26)

    # --- Buttons ---
    play_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 - 45, 200, 50),
        text="PLAY",
        font=btn_font
    )

    rod_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 + 30, 200, 50),
        text="SELECT ROD",
        font=btn_font
    )

    log_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 + 100, 200, 50),
        text="BESTINARY",
        font=btn_font
    )

    quit_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 + 170, 200, 50),
        text="QUIT",
        font=btn_font
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

            if quit_btn.clicked(event):
                return "QUIT"

        screen.fill(BG_COLOR)

        # --- Title ---
        title = title_font.render("Fishing DDA", True, (230, 230, 230))
        screen.blit(title, title.get_rect(center=(S.WIDTH//2, S.HEIGHT//2 - 130)))

        # --- Draw Buttons ---
        play_btn.draw(screen)
        rod_btn.draw(screen)
        log_btn.draw(screen)
        quit_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
