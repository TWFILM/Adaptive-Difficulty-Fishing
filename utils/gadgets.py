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
    def __init__(self, rect, fish_data, font, small_font, image, rarity="Common"):
        self.rect = pygame.Rect(rect)
        self.fish = fish_data
        self.font = font
        self.small_font = small_font
        self.rarity = rarity

        # pic area
        self.pic_size = 72
        self.pic_w = int(self.pic_size * 1.3)
        self.pic_h = self.pic_size

        title_y = self.rect.y + 18
        self.rarity_color = RARITY_COLORS.get(rarity, (180, 180, 180))

        self.image = pygame.transform.smoothscale(
            image, (self.pic_w, self.pic_h)
        )
        
        self.pic_rect = self.image.get_rect(
            center=(
                self.rect.centerx,
                title_y + self.font.get_height() + 10 + self.pic_h // 2
            )
        )

    def draw(self, screen):
        # ── Card background ──
        pygame.draw.rect(
            screen, (40, 60, 90),
            self.rect, border_radius=18
        )

        # name (center)
        title = self.font.render(
            self.fish["name"].upper(),
            True,
            self.rarity_color
        )

        # rarity bar
        pygame.draw.rect(
            screen,
            self.rarity_color,
            (self.rect.x, self.rect.y, self.rect.width, 6),
            border_radius=6
        )

        title_rect = title.get_rect(centerx=self.rect.centerx, y=self.rect.y + 16)
        screen.blit(title, title_rect)

        # image
        pygame.draw.rect(screen, (0, 0, 0), self.pic_rect, 2)
        
        # draw rarity border
        pygame.draw.rect(
            screen,
            self.rarity_color,
            self.pic_rect,
            3,
            border_radius=6
        )
        screen.blit(self.image, self.pic_rect)


        # description (center block)
        self.draw_multiline_text_center(
            screen,
            self.fish["desc"].upper(),
            self.rect.centerx,
            self.pic_rect.bottom + 12,
            self.small_font,
            self.rect.width - 40
        )

    def draw_multiline_text_center(self, surface, text, center_x, start_y, font, max_width):
        words = text.split(" ")
        lines = []
        line = ""

        for word in words:
            test = line + word + " "
            if font.size(test)[0] <= max_width:
                line = test
            else:
                lines.append(line)
                line = word + " "
        if line:
            lines.append(line)

        y = start_y
        for ln in lines:
            text_surf = font.render(ln.strip(), True, (220, 220, 220))
            rect = text_surf.get_rect(centerx=center_x, y=y)
            surface.blit(text_surf, rect)
            y += font.get_height() + 4

# ── ROD CARD CLASS ────────────────
class RodCard:
    def __init__(
        self,
        rect,
        rod_data,
        font,
        small_font,
        selected=False,
        image=None
    ):
        self.rect = pygame.Rect(rect)
        self.rod = rod_data
        self.font = font
        self.small_font = small_font
        self.selected = selected
        self.image = image

        # reserved area for image
        self.IMG_PAD = 24
        self.IMG_SIZE = 90

    # ── WORD WRAP ───────────────────
    def _render_multiline(self, text, max_width, color):
        words = text.split(" ")
        lines = []
        current = ""

        for word in words:
            test = current + word + " "
            if self.small_font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word + " "

        lines.append(current)

        return [
            self.small_font.render(line.strip(), True, color)
            for line in lines
        ]

    # ── DRAW ────────────────────────
    def draw(self, screen):
        bg = (70, 120, 200) if self.selected else (40, 60, 90)
        border = (70, 120, 200) if self.selected else None

        pygame.draw.rect(screen, bg, self.rect, border_radius=18)
        if border:
            pygame.draw.rect(screen, border, self.rect, 3, border_radius=18)

        # ── IMAGE AREA ────────────────
        img_x = self.rect.x + self.IMG_PAD
        img_y = self.rect.y + self.rect.height // 2 - self.IMG_SIZE // 2

        if self.image:
            img = pygame.transform.smoothscale(
                self.image, (self.IMG_SIZE, self.IMG_SIZE)
            )
            screen.blit(img, (img_x, img_y))
        else:
            # placeholder
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                (img_x, img_y, self.IMG_SIZE, self.IMG_SIZE),
                border_radius=12
            )

        # ── TEXT AREA ─────────────────
        text_x = img_x + self.IMG_SIZE + 24
        text_width = self.rect.right - text_x - 24

        # Title
        title = self.font.render(
            self.rod["name"].upper(), True, (240, 240, 240)
        )
        screen.blit(title, (text_x, self.rect.y + 18))

        # Stats
        y = self.rect.y + 52
        stats = [
            f"LUCK        {format_percent(self.rod.get('LUCK'))}",
            f"CONTROL     {format_number(self.rod.get('CONTROLLED'))}",
            f"RESILIENCE  {format_percent(self.rod.get('RESILIENCE'))}",
        ]


        for stat in stats:
            surf = self.small_font.render(stat, True, (210, 210, 210))
            screen.blit(surf, (text_x, y))
            y += 22

        # Description (auto wrap)
        desc_lines = self._render_multiline(
            self.rod["desc"],
            text_width,
            (220, 220, 220)
        )

        desc_y = self.rect.bottom - 20 - len(desc_lines) * 18
        for line in desc_lines:
            screen.blit(line, (text_x, desc_y))
            desc_y += 18

def format_percent(value):
    if isinstance(value, (int, float)):
        return f"{value * 100:.0f}%"
    return "N/A"

def format_number(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return "N/A"
