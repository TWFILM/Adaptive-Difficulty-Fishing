# utils/experiment_logger.py
import csv
import os
from datetime import datetime

LOG_FILE = "experiment_results.csv"
FIELDNAMES = [
    "Timestamp", 
    "Player_ID", 
    "Mode_Played", 
    "Win_Loss", 
    "Q1_Boredom", 
    "Q2_Frustration", 
    "Q3_Flow"
]

def log_experiment_data(player_id, mode, win_loss, survey_results):
    """
    Appends a new row of experiment data to the CSV file.
    
    Args:
        player_id (str): A unique identifier for the player session.
        mode (str): The difficulty mode that was just played (e.g., "EASY", "DDA").
        win_loss (str): "WIN" or "LOSS".
        survey_results (dict): A dictionary with keys 'Q1', 'Q2', 'Q3' and integer values.
    """
    
    # Create file and write header if it doesn't exist
    file_exists = os.path.isfile(LOG_FILE)
    
    row_data = {
        "Timestamp": datetime.now().isoformat(),
        "Player_ID": player_id,
        "Mode_Played": mode,
        "Win_Loss": win_loss,
        "Q1_Boredom": survey_results.get("Q1", ""),
        "Q2_Frustration": survey_results.get("Q2", ""),
        "Q3_Flow": survey_results.get("Q3", "")
    }
    
    try:
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row_data)
        print(f"[Experiment Logger] Successfully logged data for Player {player_id}, Mode {mode}.")
    except IOError as e:
        print(f"[Experiment Logger] Error writing to file: {e}")

