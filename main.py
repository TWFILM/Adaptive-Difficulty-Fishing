# main.py
import os
import uuid
# if not os.environ.get("SDL_AUDIODRIVER"):
#     os.environ["SDL_AUDIODRIVER"] = "dummy"

from interface.bestiary import run_bestiary
from interface.credits import run_credits
from interface.game import run_game
from interface.game_vertical import run_game_vertical
from interface.how_to_play import run_how_to_play
from interface.lobby import run_lobby
from interface.play_guide import run_play_guide
from interface.rod_selection import run_rod_selection
from interface.setting import run_settings
from interface.difficulty_selection import run_difficulty_selection
from interface.survey import run_survey


import pygame
from utils.scaler import build_scaled_config
from utils.save_reader import load_save
from utils.load_audio import play_lobby_sfx, stop_lobby_sfx, load_sfx
from gameData.get_info import get_unlocked_rods
from utils.load_img import load_icon_image
from utils.experiment_logger import log_experiment_data

load_sfx()


DEFAULT_SETTINGS = {
    "width": 600,
    "height": 800,
    "gameplay": "horizontal",
    "sfx": True,
    "FPS": 60
}

def main():
    pygame.init()
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
            next_state = run_lobby(screen, S, settings_data["FPS"])

            if next_state == "GAME":
                state = "DIFFICULTY_SELECTION"
            else:
                state = next_state

        elif state == "DIFFICULTY_SELECTION":
            result = run_difficulty_selection(screen, S)
            if result == "QUIT":
                state = "QUIT"
            elif result == "LOBBY":
                state = "LOBBY"
            else:
                current_difficulty = result
                state = "GAME"

        elif state == "EXPERIMENT":
            stop_lobby_sfx()
            run_play_guide(screen, S, duration=15, FPS=settings_data["FPS"])
            player_id = str(uuid.uuid4())
            experiment_modes = ["EASY", "MEDIUM", "HARD", "DDA"]
            remaining_rounds = len(experiment_modes) # Assuming 1 survey round per mode

            for mode in experiment_modes:
                save_data = load_save()
                rod_name = save_data["player"]["rod"]
                axis = settings_data["gameplay"]
                S = build_scaled_config(settings_data["width"], settings_data["height"], axis)
                screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))

                if axis == "horizontal":
                    game_result = run_game(screen, S, rod_name, settings_data["FPS"], mode, is_experiment=True)
                else:
                    game_result = run_game_vertical(screen, S, rod_name, settings_data["FPS"], mode, is_experiment=True)

                win_loss = "WIN" if game_result[0] else "LOSS"

                survey_results = run_survey(screen, S, remaining_rounds - 1)

                log_experiment_data(player_id, mode, win_loss, survey_results)
                remaining_rounds -= 1

            state = "LOBBY"
            play_lobby_sfx()

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

            if axis == "horizontal":
                game_result = run_game(screen, S, rod_name, settings_data["FPS"], current_difficulty, is_experiment=False)
            else:
                game_result = run_game_vertical(screen, S, rod_name, settings_data["FPS"], current_difficulty, is_experiment=False)

            if game_result == "RETRY":
                state = "GAME"
            else: # LOBBY or QUIT
                state = game_result

            if state == "LOBBY":
                play_lobby_sfx()

        elif state == "SELECT_ROD":
            get_unlocked_rods()
            save_data = load_save()
            unlocked_rods = save_data["player"]["unlocked_rods"]
            state = run_rod_selection(screen, S, unlocked_rods, settings_data["FPS"])

        elif state == "FISH_LOG":
            save_data = load_save()
            unlocked_fish = save_data["player"]["catched_fish"]
            state = run_bestiary(screen, S, unlocked_fish, settings_data["FPS"])

        elif state == "SETTINGS":
            state = run_settings(screen, S, settings_data)

        elif state == "HOW_TO_PLAY":
            state = run_how_to_play(screen, S, settings_data["FPS"])

        elif state == "CREDITS":
             state = run_credits(screen, S, settings_data)

    stop_lobby_sfx()
    pygame.quit()


if __name__ == "__main__":
    main()
