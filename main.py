# main.py
from game import run_game
from logger import DataLogger

def main():
    logger = DataLogger()
    success = run_game(logger)
    logger.export()

    if success:
        print("🎣 Catch success! Progress reached 100%.")
    else:
        print("❌ Game ended before completion.")

if __name__ == "__main__":
    main()
