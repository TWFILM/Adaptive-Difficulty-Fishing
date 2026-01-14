import pygame

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
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos)
        )
    
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
            f"LUCK        {int(self.rod['LUCK'] * 100)}%",
            f"CONTROL     {float(self.rod['CONTROLLED'])}" if self.rod['CONTROLLED'] != 0 else 
                f"CONTROL     {int(self.rod['CONTROLLED'])}",
            f"RESILIENCE  {int(self.rod['RESILIENCE'] * 100)}%"
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
