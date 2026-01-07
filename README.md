# Adaptive Difficulty Fishing 🎣

A research-oriented simulation project exploring **Dynamic Difficulty Adjustment (DDA)** algorithms within a Stardew Valley-inspired fishing mechanic.

This repository demonstrates how real-time user performance metrics can drive algorithmic adjustments to game parameters (e.g., hit window size, object velocity) to maintain an optimal "Flow State" for the player.

## 🧪 Project Objective

The primary goal is to study the relationship between **player performance** and **system adaptation**. The system logs gameplay data to analyze how quickly and effectively the DDA algorithm responds to player skill variance.

## ⚙️ Core Mechanics (The DDA Algorithm)

The system continuously monitors the player's tracking status (`is_catching`) and adjusts two key variables in real-time:

1.  **Bar Height (Spatial Difficulty):**
    * *Success:* Decreases size (requires more precision).
    * *Failure:* Increases size (provides assist).
2.  **Fish Speed (Temporal Difficulty):**
    * *Success:* Increases velocity multiplier.
    * *Failure:* Decreases velocity multiplier.
  
**Logic snippet:**
> If `Performance` > Threshold: Increase Difficulty ($\Delta+$ Speed, $\Delta-$ Size)
> Else: Decrease Difficulty ($\Delta-$ Speed, $\Delta+$ Size)

## 📂 Repository Structure

* `main.py`: The core simulation engine. Handles the game loop, DDA logic processing, and real-time data logging.
* `plot_graph.py`: Data visualization script. Parses the generated CSV to visualize the correlation between **Player Performance** (Catch/Miss) and **Difficulty Metrics** (Bar Size).
* `stardew_dda_result.csv`: (Generated Output) Raw dataset containing time-series data of the play session.
* `dda_graph.png`: (Generated Output) The final visualization chart showing the DDA algorithm's behavior.

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Required libraries:
    ```bash
    pip install pygame pandas matplotlib
    ```

### Usage

1.  **Run the Simulation:**
    Start the game and play. The system will auto-adjust difficulty based on your inputs.
    ```bash
    python3 main.py
    ```
    *Controls: Use `UP` and `DOWN` arrow keys to keep the fish inside the bar.*

2.  **Analyze the Data:**
    After closing the simulation, a CSV file is generated. Run the analysis script to visualize the session:
    ```bash
    python3 plot_graph.py
    ```

3.  **View Results:**
    Check `dda_graph_clean.png` to see the visualization of how the system adapted to your gameplay.

## 📊 Data Visualization

The analysis script produces a dual-axis chart:
* **Top Chart:** Binary Player State (Green = Catching, Red = Missing).
* **Bottom Chart:** Difficulty Curve (Inverted Y-axis: Higher curve = Higher difficulty/Smaller Bar).

## 🛠 Tech Stack

* **Simulation:** Pygame
* **Data Processing:** Pandas, CSV module
* **Visualization:** Matplotlib

---
*Developed for Educational & Research Purposes in Game Mechanics.*
