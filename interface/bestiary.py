import pygame
import os

from gameData.config import BG_COLOR, FPS
from gameData.get_info import get_fish_data, get_locked_fish_info  
from utils.gadgets import Button, FishCard    

# ── PATH ───────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


FONT_TITLE = os.path.join(ROOT_DIR, "assets", "fonts", "Underlines-PVjX2.ttf")
FONT_BODY  = os.path.join(ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf")

FONT_PATH1 = os.path.join(
    ROOT_DIR, "assets", "fonts", "Underlines-PVjX2.ttf"
)

FONT_PATH2 = os.path.join(
    ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf"
)

PAGE_SIZE = 4  # 2x2

def run_bestiary(screen, S, unlocked_fish):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Bestiary")
    clock = pygame.time.Clock()

    # fonts
    title_font = pygame.font.Font(FONT_PATH1, 48)
    card_font = pygame.font.Font(FONT_PATH2, 16)
    desc_font = pygame.font.Font(FONT_PATH2, 12)
    btn_font = pygame.font.Font(FONT_PATH2, 26)

    # data
    FISH_DATA = get_fish_data()          # dict
    LOCKED_INFO = get_locked_fish_info() # dict
    fish_list = list(FISH_DATA.values())

    # layout
    CARD_W = int(S.WIDTH * 0.42)
    CARD_H = int(S.HEIGHT * 0.25)

    GAP_X = 26
    GAP_Y = 26

    START_X = (S.WIDTH - (CARD_W * 2 + GAP_X)) // 2
    START_Y = int(S.HEIGHT * 0.22)

    PAGE_SIZE = 4
    page = 0

    # buttons
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
        text="LOBBY",
        font=btn_font
    )

    # ── PRELOAD CARDS (IMPORTANT) ────
    cards = []

    for rarity_group in fish_list: 
        for fish in rarity_group:            
            name = fish["name"]

            if name in unlocked_fish:
                img_path = os.path.join(
                    ROOT_DIR, "assets", "images", fish.get("img", "default.png")
                )
                data = fish
            else:
                locked = LOCKED_INFO.get(name, {})
                img_path = os.path.join(
                    ROOT_DIR, "assets", "images",
                    locked.get("img", "locked_fish.png")
                )
                data = {
                    "name": "LOCKED FISH",
                    "desc": locked.get(
                        "desc", "Catch this fish to unlock information."
                    ),
                    "rarity": "Locked"
                }

            image = pygame.image.load(img_path).convert_alpha()

            cards.append({
                "data": data,
                "image": image
            })

    # ── LOOP ────────────────────────
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"

            if back_btn.clicked(event):
                if page > 0:
                    page -= 1

            if next_btn.clicked(event):
                if (page + 1) * PAGE_SIZE < len(cards):
                    page += 1

            if center_btn.clicked(event):
                return "LOBBY"

        # draw
        screen.fill(BG_COLOR)

        # title
        title = title_font.render("Bestiary", True, (240, 240, 240))
        screen.blit(
            title,
            title.get_rect(center=(S.WIDTH // 2, S.HEIGHT * 0.12))
        )

        # cards
        start = page * PAGE_SIZE
        visible = cards[start:start + PAGE_SIZE]

        for i, item in enumerate(visible):
            col = i % 2
            row = i // 2

            x = START_X + col * (CARD_W + GAP_X)
            y = START_Y + row * (CARD_H + GAP_Y)

            card = FishCard(
                rect=(x, y, CARD_W, CARD_H),
                fish_data=item["data"],
                font=card_font,
                small_font=desc_font,
                image=item["image"],
                rarity=item["data"].get("rarity", "Common")
            )
            card.draw(screen)

        # buttons
        back_btn.draw(screen)
        center_btn.draw(screen)
        next_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)