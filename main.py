# main.py
from interface.game import run_game
from interface.lobby import run_lobby
from logger import DataLogger


def main():
    logger = DataLogger()
    state = "LOBBY"

    while state != "QUIT":
        if state == "LOBBY":
            state = run_lobby()

        elif state == "GAME":
            success = run_game(logger)
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
