# logger.py
import csv
import time

class DataLogger:
    def __init__(self):
        self.start_time = time.time()
        self.rows = []

    def log(self, bar_width, fish_speed, is_catching):
        t = round(time.time() - self.start_time, 2)
        self.rows.append([t, bar_width, round(fish_speed, 3), int(is_catching)])

    def export(self, filename="dda_result.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Bar_Width", "Fish_Speed", "Is_Catching"])
            writer.writerows(self.rows)
