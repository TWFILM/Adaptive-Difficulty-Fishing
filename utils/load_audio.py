import pygame
import os

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# FOR MEME ROD ONLY!!
def trigger_jumpscare(meme_fish=False):
    if meme_fish:
        jumpscare_path = os.path.join(BASE_DIR, "assets", "sfx", "meme_fish.wav")
    else : 
        jumpscare_path = os.path.join(BASE_DIR, "assets", "sfx", "meme.wav")
    jumpscare_sfx = pygame.mixer.Sound(jumpscare_path)

    jumpscare_sfx.set_volume(1.0) 
    jumpscare_sfx.play()

def lobby_sfx():
    pygame.mixer.init()
    lobby_path = os.path.join(BASE_DIR, "assets", "sfx", "monplaisir.wav")
    lobby_sfx = pygame.mixer.Sound(lobby_path)
    lobby_sfx.play(0)

def stop_sfx():
    pygame.mixer.stop()

stab_sfx = None

def load_stab_sfx():
    global stab_sfx
    stab_path = os.path.join(BASE_DIR, "assets", "sfx", "slash.wav")
    stab_sfx = pygame.mixer.Sound(stab_path)
    stab_sfx.set_volume(0.5) 

def play_stab_sfx():
    stab_sfx.play()