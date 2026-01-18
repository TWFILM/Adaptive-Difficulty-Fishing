import pygame
import os

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Global SFX variables
stab_sfx = None
lobby_sfx = None
meme_sfx = None
meme_fish_sfx = None
unlock_sfx = None
button_sfx = None
warned_sfx = None

def load_sfx():
    global stab_sfx, lobby_sfx, meme_sfx, meme_fish_sfx, unlock_sfx, button_sfx, warned_sfx
    
    try:
        lobby_path = os.path.join(BASE_DIR, "assets", "sfx", "monplaisir.wav")
        lobby_sfx = pygame.mixer.Sound(lobby_path)
        
        stab_path = os.path.join(BASE_DIR, "assets", "sfx", "slash.wav")
        stab_sfx = pygame.mixer.Sound(stab_path)
        stab_sfx.set_volume(0.25)
        
        meme_path = os.path.join(BASE_DIR, "assets", "sfx", "meme.wav")
        meme_sfx = pygame.mixer.Sound(meme_path)
        meme_sfx.set_volume(1.0)
        
        meme_fish_path = os.path.join(BASE_DIR, "assets", "sfx", "meme_fish.wav")
        meme_fish_sfx = pygame.mixer.Sound(meme_fish_path)
        meme_fish_sfx.set_volume(1.0)

        unlock_path = os.path.join(BASE_DIR, "assets", "sfx", "unlock.wav")
        unlock_sfx = pygame.mixer.Sound(unlock_path)
        unlock_sfx.set_volume(1.0)

        button_path = os.path.join(BASE_DIR, "assets", "sfx", "button.wav")
        button_sfx = pygame.mixer.Sound(button_path)
        button_sfx.set_volume(1.0)

        warned_path = os.path.join(BASE_DIR, "assets", "sfx", "warned.wav")
        warned_sfx = pygame.mixer.Sound(warned_path)
        warned_sfx.set_volume(1.0)
    except pygame.error as e:
        print(f"Error loading sound files: {e}")

def trigger_jumpscare(meme_fish=False):
    if meme_fish and meme_fish_sfx:
        meme_fish_sfx.play()
    elif meme_sfx:
        meme_sfx.play()

def play_lobby_sfx():
    if lobby_sfx:
        pygame.mixer.init()
        lobby_sfx.play(-1)

def play_stab_sfx():
    if stab_sfx:
        stab_sfx.play()

def stop_lobby_sfx():
    if lobby_sfx:
        lobby_sfx.stop()

def play_unlock_sfx():
    if unlock_sfx:
        unlock_sfx.play()

def play_button_sfx():
    if button_sfx:
        button_sfx.play()

def play_warned_sfx():
    if warned_sfx:
        warned_sfx.play()