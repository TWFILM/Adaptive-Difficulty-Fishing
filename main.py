# main.py
from interface.game import run_game
from interface.lobby import run_lobby
from interface.rod_selection import run_rod_selection
from logger import DataLogger

import pygame
from gameData.scaler import build_scaled_config
from gameData.save_reader import load_save


def main():
    logger = DataLogger()
    state = "LOBBY"

    while state != "QUIT":
        if state == "LOBBY":
            pygame.init()
            S = build_scaled_config()   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            state = run_lobby(screen, S)

        elif state == "GAME":
            # load player selection rod
            save_data = load_save()
            rod_name = save_data["player"]["rod"]
            print(rod_name)
            pygame.init()
            S = build_scaled_config()   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            
            success = run_game(screen, S, logger, rod_name)
            print("Game Result:", "🎣 Catch success! Progress reached 100%." if success else "❌ Game ended before completion.")
            state = "LOBBY"

        elif state == "SELECT_ROD":
            pygame.init()
            S = build_scaled_config()   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            state = run_rod_selection(screen, S)

        elif state == "FISH_LOG":
            print("BESTINARY (ยังไม่ทำ)")
            state = "LOBBY"

if __name__ == "__main__":
    main()
