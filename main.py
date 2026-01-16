# main.py
from interface.game import run_game
from interface.game_vertical import run_game_vertical
from interface.lobby import run_lobby
from interface.rod_selection import run_rod_selection
from logger import DataLogger

import pygame
from utils.scaler import build_scaled_config
from utils.save_reader import load_save
from utils.load_audio import lobby_sfx, stop_sfx


def main():
    logger = DataLogger()
    state = "LOBBY"
    lobby_sfx()

    while state != "QUIT":
        if state == "LOBBY":
            pygame.init()
            S = build_scaled_config()   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            state = run_lobby(screen, S)
            
        elif state == "GAME":
            # load player selection rod
            stop_sfx()
            save_data = load_save()
            rod_name = save_data["player"]["rod"]
            axis = save_data["player"]["default"]
            # print(rod_name)
            pygame.init()
            S = build_scaled_config(axis)   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            if axis == "horizontal":
                success = run_game(screen, S, logger, rod_name)
            else:
                success = run_game_vertical(screen, S, logger, rod_name)
            print("Game Result:", f"🎣 Catch success! You caught the {success[1]} {success[2]}." if success[0] else "❌ Game ended the fish got away...")
            state = "LOBBY"
            lobby_sfx()

        elif state == "SELECT_ROD":
            pygame.init()
            save_data = load_save()
            unlocked_rods = save_data["player"]["unlocked_rods"]
            S = build_scaled_config()   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            state = run_rod_selection(screen, S, unlocked_rods)

        elif state == "FISH_LOG":
            print("BESTIARY (ยังไม่ทำ)")
            state = "LOBBY"

    stop_sfx()

if __name__ == "__main__":
    main()
