# main.py
from interface.game import run_game
from interface.lobby import run_lobby
from logger import DataLogger

import pygame
from gameData.scaler import build_scaled_config


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
            pygame.init()
            S = build_scaled_config()   
            screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
            success = run_game(screen, S, logger)
            print("Game Result:", "🎣 Catch success! Progress reached 100%." if success else "❌ Game ended before completion.")
            state = "LOBBY"

        elif state == "SELECT_ROD":
            print("SELECT ROD (ยังไม่ทำ)")
            state = "LOBBY"

        elif state == "FISH_LOG":
            print("BESTINARY (ยังไม่ทำ)")
            state = "LOBBY"

if __name__ == "__main__":
    main()
