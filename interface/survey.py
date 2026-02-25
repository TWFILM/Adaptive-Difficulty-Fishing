# interface/survey.py
import pygame
import os

from gameData.config import BG_COLOR
from utils.load_img import load_ui_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FONT_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf")

QUESTIONS = [
    "How BORING was this mode?",
    "How STRESSFUL was this mode?",
    "How FOCUSED and 'in the zone' were you?"
]

SCALE_TEXT = "(1 = Not at all, 5 = Extremely)"

def draw_text(screen, text, font, color, center_x, center_y, bg_color=None):
    text_surface = font.render(text, True, color, bg_color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

def run_survey(screen, S, mode, remaining_survey=2):
    pygame.init()
    clock = pygame.time.Clock()

    bg_img = load_ui_image("game_bg2.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))
    
    font_title = pygame.font.Font(FONT_PATH, int(30 * S.scale))
    font_question = pygame.font.Font(FONT_PATH, int(22 * S.scale))
    font_scale = pygame.font.Font(FONT_PATH, int(18 * S.scale))
    
    answers = {}
    current_question = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Return incomplete results if the user quits
                return answers
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    answer = event.key - pygame.K_0
                    answers[f"Q{current_question + 1}"] = answer
                    current_question += 1
                    if current_question >= len(QUESTIONS):
                        running = False
        
        screen.blit(bg_img, (0, 0))
        
        # Draw Title
        draw_text(screen, "Post-Game Survey", font_title, (255, 255, 255), S.WIDTH // 2, S.HEIGHT * 0.2)
        
        if current_question < len(QUESTIONS):
            # Draw current question
            draw_text(screen, QUESTIONS[current_question], font_question, (200, 200, 200), S.WIDTH // 2, S.HEIGHT * 0.4)
            draw_text(screen, SCALE_TEXT, font_scale, (170, 170, 170), S.WIDTH // 2, S.HEIGHT * 0.45)

            # Draw response boxes/prompts
            prompt = "Please press a number key (1-5) to answer."
            draw_text(screen, prompt, font_scale, (255, 255, 100), S.WIDTH // 2, S.HEIGHT * 0.6)

            for i in range(1, 6):
                draw_text(screen, str(i), font_question, (255, 255, 255), S.WIDTH // 2 + (i - 3) * 60 * S.scale, S.HEIGHT * 0.7)
        else:
            # All questions answered
            draw_text(screen, f"Thank you! Another {remaining_survey} left" if remaining_survey > 0 else "Thank you! for surveying" , font_title, (100, 255, 100), S.WIDTH // 2, S.HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(1500) # Show "Thank you" for a moment
            running = False

        pygame.display.flip()
        clock.tick(30)
        
    return answers
