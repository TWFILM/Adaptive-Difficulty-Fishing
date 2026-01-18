import pygame
import os

from gameData.config import BG_COLOR, FPS
from gameData.get_info import get_rod_des, get_locked_rod_info
from utils.save_writer import SaveManager
from utils.gadgets import Button, RodCard
from utils.load_audio import play_unlock_sfx, play_warned_sfx

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
LOCKED_RODS = get_locked_rod_info()  # dict
rod_data = list(RODS.values())

def run_rod_selection(screen, S, unlocked_rods):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Rod Selection")
    clock = pygame.time.Clock()

    # ── FONTS ───────────────────────
    title_font = pygame.font.Font(FONT_PATH1, 48)
    card_title_font = pygame.font.Font(FONT_PATH2, 24)
    card_desc_font = pygame.font.Font(FONT_PATH2, 17)
    btn_font = pygame.font.Font(FONT_PATH2, 26)
    status_font = pygame.font.Font(FONT_PATH2, 20)

    # ── LAYOUT ──────────────────────
    CARD_WIDTH = int(S.WIDTH * 0.8)
    CARD_HEIGHT = int(S.HEIGHT * 0.22)
    CARD_X = (S.WIDTH - CARD_WIDTH) // 2

    START_Y = int(S.HEIGHT * 0.25)
    GAP = int(S.HEIGHT * 0.05)

    warning_text = ""
    warning_time = 0
    WARNING_DURATION = 2000

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

    # ── UNLOCK WARNING CHECK ──────────────────
    save = SaveManager()

    unlock_queue = []          
    warning_text = None
    warning_time = 0
    WARNING_DURATION = 2500    # ms
    sound_played = False

    shown = save.data["player"].setdefault("shown_unlock_notice", [])

    for rod_name in unlocked_rods:
        if rod_name not in shown:
            unlock_queue.append(f"New Rod Unlocked: {rod_name}!")
            shown.append(rod_name)

    if unlock_queue:
        play_unlock_sfx()
        if warning_text and not sound_played:
            sound_played = True

        save.save()
        warning_text = unlock_queue.pop(0)
        warning_time = pygame.time.get_ticks()

    

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

                if chosen_rod["name"] not in unlocked_rods:
                    warning_text = "You must unlock this rod first"
                    play_warned_sfx()
                    warning_time = pygame.time.get_ticks()
                else:
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
            rod_name = rod["name"]

            if is_selected:
                current_hover_rod = rod_name
                current_hover_locked = rod_name not in unlocked_rods

            if rod_name in unlocked_rods:
                image_path = os.path.join(
                    ROOT_DIR, "assets", "images", rod.get("img", "default.png")
                )

                card = RodCard(
                    rect=(CARD_X, y, CARD_WIDTH, CARD_HEIGHT),
                    rod_data=rod,
                    font=card_title_font,
                    small_font=card_desc_font,
                    selected=is_selected,
                    image=pygame.image.load(image_path).convert_alpha()
                )
            else:
                locked_info = LOCKED_RODS.get(rod_name, {})

                card = RodCard(
                    rect=(CARD_X, y, CARD_WIDTH, CARD_HEIGHT),
                    rod_data={
                        "name": "Locked Rod",
                        "desc": locked_info.get(
                            "desc", "Unlock this rod to view details."
                        ),
                        "LUCK": "?",
                        "CONTROLLED": "?",
                        "RESILIENCE": "?"
                    },
                    font=card_title_font,
                    small_font=card_desc_font,
                    selected=is_selected,
                    image=pygame.image.load(
                        os.path.join(
                            ROOT_DIR,
                            "assets",
                            "images",
                            locked_info.get("img", "locked_rod.png")
                        )
                    ).convert_alpha()
                )

            card.draw(screen)
      
        # ── WARNING TEXT ──────────────────
        if warning_text:
            elapsed = pygame.time.get_ticks() - warning_time

            if elapsed < WARNING_DURATION:
                alpha = max(0, 255 - int((elapsed / WARNING_DURATION) * 255))

                warn_surf = btn_font.render(
                    warning_text, True, (255, 215, 120) if "Unlocked" in warning_text else (255, 90, 90)
                )
                warn_surf.set_alpha(alpha)

                screen.blit(
                    warn_surf,
                    warn_surf.get_rect(
                        center=(S.WIDTH // 2, int(S.HEIGHT * 0.2))
                    )
                )

            else:
                # current message done → show next
                if unlock_queue:
                    warning_text = unlock_queue.pop(0)
                    warning_time = pygame.time.get_ticks()
                else:
                    warning_text = None

        
        # ── CURRENT SELECTION TEXT ─────────
        if current_hover_rod:
            if current_hover_locked:
                text = f"Locked Rod: N/A"
                color = (255, 120, 120)
            else:
                text = f"Currently Selecting: {current_hover_rod}"
                color = (180, 220, 255)

            status_surf = status_font.render(text, True, color)
            screen.blit(
                status_surf,
                status_surf.get_rect(
                    center=(S.WIDTH // 2, int(S.HEIGHT * 0.77))
                )
            )

        # Buttons
        back_btn.draw(screen)
        center_btn.draw(screen)
        next_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
