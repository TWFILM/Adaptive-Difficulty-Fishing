# interface/end_screen.py
import pygame
import time
import os
import random
from gameData.config import WIDTH, HEIGHT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_end_screen_meme(screen, clock, duration=4, meme_fish=False):
    if meme_fish:
        image_path= os.path.join(BASE_DIR, "assets", "images", f"meme_fish.png")
    else :
        image_path= os.path.join(BASE_DIR, "assets", "images", f"meme{random.randint(1,5)}.png")


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

ROD_IMAGES = {}

def load_images(rod_name):
    global ROD_IMAGES

    try:
        img_path = os.path.join(
            BASE_DIR, "assets", "images", f"{rod_name}.png"
        )

        # fallback path
        fallback_path = os.path.join(
            BASE_DIR, "assets", "images", "Novice Rod.png"
        )

        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
        else:
            img = pygame.image.load(fallback_path).convert_alpha()

        img = pygame.transform.rotate(img, 110)
        ROD_IMAGES[rod_name] = img

    except pygame.error as e:
        print(f"[IMAGE LOAD ERROR] {rod_name}: {e}")

