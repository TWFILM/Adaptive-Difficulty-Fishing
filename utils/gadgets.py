import pygame

from utils.load_audio import play_button_sfx

RARITY_COLORS = {
    "Common":     (180, 180, 180),
    "Uncommon":   (120, 220, 120),
    "Rare":       (100, 180, 255),
    "Legendary":  (255, 200, 80),
    "Mythical":   (220, 120, 255),
    "Meme":       (255, 100, 120),
    "Locked":     (90, 90, 90)
}

# ── BUTTON CLASS ──────────────────
class Button:
    def __init__(self, rect, text, font,
                 bg_color=(70, 70, 70),
                 hover_color=(120, 120, 120),
                 text_color=(255, 255, 255)):

        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                play_button_sfx()
                return True
        return False

# ── FISH CARD CLASS ────────────────
class FishCard:
    def __init__(self, rect, fish_data, font, small_font,
                 image=None, rarity="Common"):
        self.rect = pygame.Rect(rect)
        self.fish = fish_data
        self.font = font
        self.small_font = small_font
        self.image = image
        self.rarity = rarity

        # ── RARITY COLOR ─────────────────
        self.rarity_color = RARITY_COLORS.get(rarity, (180, 180, 180))

        # ── IMAGE BOX CONFIG  ─────────
        self.IMG_BOX_W = 120     
        self.IMG_BOX_H = 90
        self.IMG_PAD_TOP = 40

        self.img_rect = None     #  click 

    def draw(self, screen):
        # ── CARD BACKGROUND ──────────────
        pygame.draw.rect(
            screen,
            (40, 60, 90),
            self.rect,
            border_radius=18
        )

        # ── RARITY BAR ───────────────────
        pygame.draw.rect(
            screen,
            self.rarity_color,
            (self.rect.x, self.rect.y, self.rect.width, 6),
            border_radius=6
        )

        # ── TITLE  ────────────────────────
        title = self.font.render(
            self.fish["name"].upper(),
            True,
            self.rarity_color
        )
        title_rect = title.get_rect(
            centerx=self.rect.centerx,
            y=self.rect.y + 14
        )
        screen.blit(title, title_rect)

        # ── IMAGE AREA  ─
        img_x = self.rect.centerx - self.IMG_BOX_W // 2
        img_y = self.rect.y + self.IMG_PAD_TOP

        if self.image:
            img = scale_to_fit(
                self.image,
                self.IMG_BOX_W,
                self.IMG_BOX_H
            )
            self.img_rect = img.get_rect(
                center=(
                    self.rect.centerx,
                    img_y + self.IMG_BOX_H // 2
                )
            )

            # border
            pygame.draw.rect(
                screen,
                self.rarity_color,
                self.img_rect.inflate(6, 6),
                3,
                border_radius=8
            )

            screen.blit(img, self.img_rect)
        else:
            self.img_rect = pygame.Rect(
                img_x, img_y,
                self.IMG_BOX_W,
                self.IMG_BOX_H
            )
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                self.img_rect,
                border_radius=8
            )

        # ── DESCRIPTION ─
        desc_y = self.img_rect.bottom + 12
        self.draw_multiline_text_center(
            screen,
            self.fish.get("desc", "").upper(),
            self.rect.centerx,
            desc_y,
            self.small_font,
            self.rect.width - 32
        )

    # ── CLICK CHECK ─────────────────
    def image_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.img_rect
            and self.img_rect.collidepoint(event.pos)
        )

    # ── TEXT WRAP CENTER ─────────────────
    def draw_multiline_text_center(
        self, surface, text, center_x, start_y, font, max_width
    ):
        words = text.split(" ")
        lines, line = [], ""

        for w in words:
            test = line + w + " "
            if font.size(test)[0] <= max_width:
                line = test
            else:
                lines.append(line)
                line = w + " "

        if line:
            lines.append(line)

        y = start_y
        for ln in lines:
            surf = font.render(ln.strip(), True, (220, 220, 220))
            rect = surf.get_rect(centerx=center_x, y=y)
            surface.blit(surf, rect)
            y += font.get_height() + 4


# ── ROD CARD CLASS ────────────────
class RodCard:
    def __init__(self, rect, rod_data, font, small_font,
                 selected=False, image=None):
        self.rect = pygame.Rect(rect)
        self.rod = rod_data
        self.font = font
        self.small_font = small_font
        self.selected = selected
        self.image = image

        # image box
        self.IMG_PAD = 24
        self.IMG_BOX_W = 110
        self.IMG_BOX_H = 140

        self.img_rect = None  # Check if clicked

    def draw(self, screen):
        bg = (70, 120, 200) if self.selected else (40, 60, 90)
        pygame.draw.rect(screen, bg, self.rect, border_radius=18)

        # ── IMAGE ───────────────────
        img_x = self.rect.x + self.IMG_PAD
        img_y = self.rect.centery - self.IMG_BOX_H // 2

        if self.image:
            img = scale_to_fit(self.image, self.IMG_BOX_W, self.IMG_BOX_H)
            self.img_rect = img.get_rect(
                center=(img_x + self.IMG_BOX_W // 2,
                        img_y + self.IMG_BOX_H // 2)
            )
            screen.blit(img, self.img_rect)
        else:
            self.img_rect = pygame.Rect(img_x, img_y, self.IMG_BOX_W, self.IMG_BOX_H)
            pygame.draw.rect(screen, (30, 30, 30), self.img_rect, border_radius=8)

        # ── TEXT ────────────────────
        text_x = img_x + self.IMG_BOX_W + 24

        title = self.font.render(self.rod["name"].upper(), True, (240, 240, 240))
        screen.blit(title, (text_x, self.rect.y + 18))

        y = self.rect.y + 52
        stats = [
            f"LUCK        {self.rod.get('LUCK', 'N/A')}",
            f"CONTROL     {self.rod.get('CONTROLLED', 'N/A')}",
            f"RESILIENCE  {self.rod.get('RESILIENCE', 'N/A')}",
        ]
        for s in stats:
            screen.blit(self.small_font.render(s, True, (210, 210, 210)), (text_x, y))
            y += 22

        desc_lines = wrap_text(
            self.rod.get("desc", ""),
            self.small_font,
            self.rect.right - text_x - 24
        )

        dy = self.rect.bottom - 20 - len(desc_lines) * 18
        for ln in desc_lines:
            screen.blit(self.small_font.render(ln, True, (220, 220, 220)), (text_x, dy))
            dy += 18

    def image_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.img_rect
            and self.img_rect.collidepoint(event.pos)
        )
    


# ── HELPERS ─────────────────────────
def scale_to_fit(img, max_w, max_h):
    w, h = img.get_size()
    s = min(max_w / w, max_h / h)
    return pygame.transform.smoothscale(img, (int(w * s), int(h * s)))

def wrap_text(text, font, max_w):
    words = text.split(" ")
    lines, line = [], ""
    for w in words:
        test = line + w + " "
        if font.size(test)[0] <= max_w:
            line = test
        else:
            lines.append(line.strip())
            line = w + " "
    if line:
        lines.append(line.strip())
    return lines

def format_percent(value):
    if isinstance(value, (int, float)):
        return f"{value * 100:.0f}%"
    return "N/A"

def format_number(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return "N/A"

def scale_to_fit(image, max_w, max_h):
    w, h = image.get_size()
    scale = min(max_w / w, max_h / h)
    return pygame.transform.smoothscale(
        image,
        (int(w * scale), int(h * scale))
    )