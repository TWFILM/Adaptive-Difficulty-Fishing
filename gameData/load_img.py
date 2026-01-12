# interface/end_screen.py
import pygame
import time
import os
import random
from gameData.config import WIDTH, HEIGHT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_end_screen_meme(screen, clock, duration=4):
    IMG_PATH = os.path.join(BASE_DIR, "assets", "images", f"meme{random.randint(1,3)}.png")
    image_path = IMG_PATH

    end_image = pygame.image.load(image_path).convert_alpha()
    end_image = pygame.transform.scale(end_image, (WIDTH, HEIGHT))

    start_time = time.time()
    image_rect = end_image.get_rect(
        center=(WIDTH // 2, HEIGHT // 2)
    )
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        screen.blit(end_image, image_rect)

        pygame.display.flip()
        clock.tick(60)
