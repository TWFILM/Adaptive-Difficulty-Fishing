import pygame
import os
from gameData.config import BG_COLOR, FPS
from utils.save_writer import SaveManager
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

def run_rod_selection(screen, S):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Fishing Lobby")
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(FONT_PATH1, 42)
    btn_font = pygame.font.Font(FONT_PATH2, 26)

    # --- Buttons ---
    novice_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 - 170, 200, 50),
        text="NOVICE ROD",
        font=btn_font
    )

    cool_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 - 100, 200, 50),
        text="COOL ROD",
        font=btn_font
    )

    rus_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 - 30, 200, 50),
        text="RU SURE ROD",
        font=btn_font
    )

    pris_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 + 40, 200, 50),
        text="PRISMATIC ROD",
        font=btn_font
    )

    back_btn = Button(
        rect=(S.WIDTH//2 - 100, S.HEIGHT//2 + 110, 200, 50),
        text="BACK TO GAME",
        font=btn_font
    )

    running = True
    while running:
        for event in pygame.event.get():
            if novice_btn.clicked(event):
                save = SaveManager()
                save.data["player"]["rod"] = "Novice Rod"
                save.save()
                print("You are currently using Novice Rod!")

            if cool_btn.clicked(event):
                save = SaveManager()
                save.data["player"]["rod"] = "Cool Rod"
                save.save()
                print("You are currently using Cool Rod!")

            if rus_btn.clicked(event):
                save = SaveManager()
                save.data["player"]["rod"] = "RU Sure Rod"
                save.save()
                print("You are currently using RU Sure Rod!")

            if pris_btn.clicked(event):
                save = SaveManager()
                save.data["player"]["rod"] = "Prismatic Rod"
                save.save()
                print("You are currently using Prismatic Rod!")
            
            if back_btn.clicked(event):
                return "LOBBY"

        screen.fill(BG_COLOR)

        # --- Title ---
        title = title_font.render("Rod", True, (230, 230, 230))
        screen.blit(title, title.get_rect(center=(S.WIDTH//2, S.HEIGHT//2 - 250)))

        # --- Draw Buttons ---
        novice_btn.draw(screen)
        cool_btn.draw(screen)
        rus_btn.draw(screen)
        pris_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
