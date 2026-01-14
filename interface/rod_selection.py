import pygame
import os

from gameData.config import BG_COLOR, FPS
from gameData.get_info import get_rod_des
from utils.save_writer import SaveManager
from interface.gadgets import Button, RodCard

# ── PATH ───────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH1 = os.path.join(
    ROOT_DIR, "assets", "fonts", "Underlines-PVjX2.ttf"
)

FONT_PATH2 = os.path.join(
    ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf"
)

# ── DATA ───────────────────────────
RODS = get_rod_des()   # list[dict]
rod_data = list(RODS.values())

def run_rod_selection(screen, S):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Rod Selection")
    clock = pygame.time.Clock()

    # ── FONTS ───────────────────────
    title_font = pygame.font.Font(FONT_PATH1, 48)
    card_title_font = pygame.font.Font(FONT_PATH2, 24)
    card_desc_font = pygame.font.Font(FONT_PATH2, 17)
    btn_font = pygame.font.Font(FONT_PATH2, 26)

    # ── LAYOUT ──────────────────────
    CARD_WIDTH = int(S.WIDTH * 0.8)
    CARD_HEIGHT = int(S.HEIGHT * 0.22)
    CARD_X = (S.WIDTH - CARD_WIDTH) // 2

    START_Y = int(S.HEIGHT * 0.25)
    GAP = int(S.HEIGHT * 0.05)

    # ── CREATE ROD CARDS (ONCE) ─────
    cards = []
    for i, rod in enumerate(rod_data):
        rect = (
            CARD_X,
            START_Y + i * (CARD_HEIGHT + GAP),
            CARD_WIDTH,
            CARD_HEIGHT
        )
        cards.append(
            RodCard(
                rect=rect,
                rod_data=rod,
                font=card_title_font,
                small_font=card_desc_font
            )
        )

    # ── BUTTONS ─────────────────────
    back_btn = Button(
        rect=(S.WIDTH * 0.18 - 80, S.HEIGHT * 0.80, 160, 60),
        text="BACK",
        font=btn_font
    )

    next_btn = Button(
        rect=(S.WIDTH * 0.82 - 80, S.HEIGHT * 0.80, 160, 60),
        text="NEXT",
        font=btn_font
    )

    center_btn = Button(
        rect=(S.WIDTH // 2 - 90, S.HEIGHT * 0.80, 180, 60),
        text="SELECT",
        font=btn_font
    )
    page_index = 0      # หน้า
    cursor = 0          # 0 = card บน, 1 = card ล่าง
    PAGE_SIZE = 2

    start = page_index * PAGE_SIZE
    visible_rods = rod_data[start : start + PAGE_SIZE]

    # ── LOOP ────────────────────────
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"

            if back_btn.clicked(event):
                if cursor > 0:
                    cursor -= 1
                else:
                    if page_index > 0:
                        page_index -= 1
                        cursor = 1

            if next_btn.clicked(event):
                if cursor + 1 < len(visible_rods):
                    cursor += 1
                else:
                    # press to go to the next page
                    if start + PAGE_SIZE < len(rod_data):
                        page_index += 1
                        cursor = 0


            if center_btn.clicked(event):
                save = SaveManager()
                chosen_rod = visible_rods[cursor]
                save.data["player"]["rod"] = chosen_rod["name"]
                save.save()
                return "LOBBY"

        # ── DRAW ─────────────────────
        screen.fill(BG_COLOR)

        start = page_index * PAGE_SIZE
        visible_rods = rod_data[start : start + PAGE_SIZE]


        # Title
        title = title_font.render("Rod Selection", True, (240, 240, 240))
        screen.blit(
            title,
            title.get_rect(center=(S.WIDTH // 2, S.HEIGHT * 0.1))
        )

        # Cards
        if len(visible_rods) == 2:
            y_positions = [
                S.HEIGHT // 2 - CARD_HEIGHT - 10,
                S.HEIGHT // 2 + 10
            ]
        else:
            y_positions = [
                S.HEIGHT // 2 - CARD_HEIGHT // 2
            ]


        for i, (rod, y) in enumerate(zip(visible_rods, y_positions)):
            is_selected = (i == cursor)
            # LOAD IMG
            image_path = os.path.join(ROOT_DIR, "assets", "images", f"{rod_data[i]["img"]}")

            card = RodCard(
                rect=(CARD_X, y, CARD_WIDTH, CARD_HEIGHT),
                rod_data=rod,
                font=card_title_font,
                small_font=card_desc_font,
                selected=is_selected,
                image=pygame.image.load(image_path).convert_alpha()
            )
            card.draw(screen)

        # Buttons
        back_btn.draw(screen)
        center_btn.draw(screen)
        next_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
