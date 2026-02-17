# main.py
import os
# os.environ["SDL_AUDIODRIVER"] = "dummy"

from interface.bestiary import run_bestiary
from interface.game import run_game
from interface.game_vertical import run_game_vertical
from interface.lobby import run_lobby
from interface.rod_selection import run_rod_selection
from interface.setting import run_settings
from interface.difficulty_selection import run_difficulty_selection
from logger import DataLogger

import pygame
from utils.scaler import build_scaled_config
from utils.save_reader import load_save
from utils.load_audio import play_lobby_sfx, stop_lobby_sfx, load_sfx, play_meme_sfx
from gameData.get_info import get_unlocked_rods
from utils.load_img import load_icon_image

load_sfx()

DEFAULT_SETTINGS = {
    "width": 600,
    "height": 800,
    "gameplay": "horizontal",
    "sfx": True,
    "mode": "Default"
}

def main():
    pygame.init()

    logger = DataLogger()
    state = "LOBBY"
    
    play_lobby_sfx()

    settings_data = load_save().get("settings_data", DEFAULT_SETTINGS)
    if settings_data["sfx"] is False:
        pygame.mixer.pause()

    # create scaled config based on saved settings (or default)
    S = build_scaled_config(
        settings_data["width"],
        settings_data["height"],
        settings_data["gameplay"]
    )
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))

    icon_img = load_icon_image()
    pygame.display.set_icon(icon_img)
    
    current_difficulty = "DDA"

    while state != "QUIT":

        # Reload settings each loop to reflect any changes made in the settings menu
        settings_data = load_save().get("settings_data", DEFAULT_SETTINGS)

        S = build_scaled_config(
            settings_data["width"],
            settings_data["height"],
            settings_data["gameplay"]
        )
        screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))

        if settings_data["sfx"] is True:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()

        if state == "LOBBY":
            next_state = run_lobby(screen, S)

            if next_state == "GAME":
                state = "DIFFICULTY_SELECTION"
            else:
                state = next_state

        elif state == "DIFFICULTY_SELECTION":
            result = run_difficulty_selection(screen, S)
            if result == "QUIT":
                state = "QUIT"
            else:
                current_difficulty = result
                state = "GAME"

        elif state == "GAME":
            stop_lobby_sfx()

            save_data = load_save()
            rod_name = save_data["player"]["rod"]
            axis = settings_data["gameplay"]

            # Rebuild scaled config in case gameplay axis or resolution was changed in settings
            S = build_scaled_config(
                settings_data["width"],
                settings_data["height"],
                axis
            )
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))

            if rod_name == "Meme Rod":
                play_meme_sfx()

            if axis == "horizontal":
                success = run_game(screen, S, logger, rod_name, current_difficulty)
            else:
                success = run_game_vertical(screen, S, logger, rod_name, current_difficulty)

            print(
                "Game Result:",
                f"🎣 Catch success! You caught the {success[1]} {success[2]}."
                if success[0]
                else "❌ Game ended the fish got away..."
            )

            state = "LOBBY"
            play_lobby_sfx()

        elif state == "SELECT_ROD":
            get_unlocked_rods()
            save_data = load_save()
            unlocked_rods = save_data["player"]["unlocked_rods"]
            state = run_rod_selection(screen, S, unlocked_rods)

        elif state == "FISH_LOG":
            save_data = load_save()
            unlocked_fish = save_data["player"]["catched_fish"]
            state = run_bestiary(screen, S, unlocked_fish)

        elif state == "SETTINGS":
            state = run_settings(screen, S, settings_data)

    stop_lobby_sfx()
    pygame.quit()


if __name__ == "__main__":
    main()
