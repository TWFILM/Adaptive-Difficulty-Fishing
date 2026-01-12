# Adaptive Difficulty Fishing 🎣

A research-oriented simulation project exploring **Dynamic Difficulty Adjustment (DDA)** algorithms within a fishing mechanic.

This repository demonstrates how real-time user performance metrics can drive algorithmic adjustments to game parameters (specifically **Fish Speed**) to maintain an optimal "Flow State" for the player.

## 🧪 Project Objective

The primary goal is to study the relationship between **player performance** and **system adaptation**. The system logs gameplay data to analyze how the DDA algorithm responds to player skill variance.

## ⚙️ Core Mechanics (The DDA Algorithm)

The system continuously monitors the player's tracking status (`is_catching`) and adjusts the difficulty in real-time:

**Fish Speed (Temporal Difficulty):**
* **Success (Catching):** The fish moves faster (Speed increases).
* **Failure (Missing):** The fish slows down (Speed decreases).

**Logic snippet:**
> If `is_catching` is True: Increase Fish Speed (Max 3.0)
> Else: Decrease Fish Speed (Min 0.5)

*(Note: Currently, the Bar Width is fixed at 120px and defined in `config.py`)*

## 🎮 Controls & Physics

The game simulates a fishing bar fighting against a water current.
* **Mouse Click (Hold):** Apply force to move the bar to the **Right**.
* **Release Mouse:** The bar naturally drifts to the **Left** due to current/friction.

**Goal:** Keep the green bar overlapping with the red fish to fill the progress bar.

## 📂 Repository Structure

* `main.py`: Entry point of the application.
* `game.py`: Handles the main game loop, physics engine, and rendering.
* `dda.py`: Contains the Dynamic Difficulty Adjustment logic.
* `config.py`: Stores constant variables (Screen size, Colors, Fixed physics values).
* `logger.py`: Handles data recording during the session.
* `fish_data.json` & `get_info.py`: Database of fish types with different resilience traits.
* `plot_graph.py`: Visualization script to generate performance charts.
* `dda_result.csv`: (Generated Output) Raw gameplay data.
* `dda_graph.png`: (Generated Output) Visualization of the session.

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Required libraries:
    ```bash
    pip install pygame pandas matplotlib
    ```

### Usage

1.  **Run the Simulation:**
    Start the game and play.
    ```bash
    python main.py
    ```

2.  **Analyze the Data:**
    After closing the simulation (or finishing the catch), a CSV file is generated. Run the analysis script:
    ```bash
    python plot_graph.py
    ```

3.  **View Results:**
    Check `dda_graph.png` to see the visualization of your performance vs. fish speed adaptation.

## 📊 Data Visualization

The analysis script produces a dual-axis chart:
* **Top Chart:** Binary Player State (Green = Catching, Red = Missing).
* **Bottom Chart:** Difficulty Curve (Inverted Y-axis logic applied if plotting bar size, or standard for speed).

## 🛠 Tech Stack

* **Simulation:** Pygame
* **Data Processing:** Pandas, CSV module
* **Visualization:** Matplotlib

---
*Developed for Educational & Research Purposes in Game Mechanics.*
