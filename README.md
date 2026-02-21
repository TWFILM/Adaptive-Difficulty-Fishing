# Dynamic Difficulty Adjustment for Flow State Optimization in a Simulated Environment

## 1. Abstract

This project presents a research tool designed to investigate the relationship between **Dynamic Difficulty Adjustment (DDA)** and the psychological concept of **Flow State** within a video game context. The simulator, developed using Pygame, implements a fishing mini-game where difficulty parameters are manipulated in real-time based on player performance. By comparing player experiences under fixed difficulty settings (Easy, Medium, Hard) against a DDA-driven model, this study aims to evaluate how algorithmic adjustments can foster a more consistent state of engagement, as described by Flow Theory. Data is collected through in-game performance metrics and post-session subjective surveys to provide a quantitative and qualitative analysis of the DDA's efficacy.

## 2. Research Objectives

The primary objective is to determine whether a DDA system is more effective at inducing and maintaining a Flow State in players compared to traditional static difficulty levels.

This is achieved by:
*   Exposing participants to four distinct, sequential gameplay conditions in a **fixed sequential order (EASY → MEDIUM → HARD → DDA)**.
*   Measuring player performance objectively through in-game metrics (e.g., time-on-target).
*   Collecting subjective feedback on player experience (Boredom, Frustration, Focus) using a mandatory mini-survey after each condition.
*   Analyzing the resulting dataset to correlate difficulty models with player-reported states of engagement.

## 3. Features for Research

This simulator was built with specific features to ensure a controlled and effective research process:

*   **Fixed Sequential Experiment Loop:** The system automatically guides the participant through the four required conditions in a fixed order (EASY → MEDIUM → HARD → DDA) to ensure consistent data collection.
*   **Controlled Variables:** To eliminate confounding variables, all experiment sessions lock the fish type to **"Shrimp"** and disable any special abilities from equipped fishing rods, ensuring that the only variable being tested is the difficulty algorithm.
*   **Mini-Survey Integration:** A brief, mandatory survey is presented after each of the four gameplay modes. This allows for the immediate capture of subjective feedback on Boredom, Frustration, and Focus, linking a player's psychological state directly to the condition they just experienced.
*   **Automated CSV Data Logging:** All experimental data, including a timestamp, the participant's unique ID, the difficulty condition, the win/loss outcome, and their survey responses are automatically logged to a single, clean CSV file (`experiment_results.csv`) for straightforward analysis.

## 4. Installation & Setup

### Prerequisites
*   Python 3.8+
*   Git

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install required libraries:**
    The project requires several libraries for the simulation, data handling, and plotting.
    ```bash
    pip install pygame pandas numpy matplotlib
    ```

## 5. How to Conduct the Experiment

This guide provides the exact steps for a researcher or participant to complete one full experimental session.

1.  **Launch the Program:**
    From the project's root directory, run the `main.py` script.
    ```bash
    python main.py
    ```

2.  **Start the Experiment:**
    In the main lobby screen, click the **"EXPERIMENT"** button. This will initiate the sequential research session.

3.  **Play Through the Four Conditions:**
    You will be automatically presented with four fishing sessions. Play each one to the best of your ability. The order is fixed:
    *   **Condition 1: EASY**
    *   **Condition 2: MEDIUM**
    *   **Condition 3: HARD**
    *   **Condition 4: DDA**

4.  **Complete the Post-Game Surveys:**
    After *each* of the four sessions, a survey will appear on the screen. You **must answer the questions by pressing the number keys (1 to 5) on the keyboard, and it will automatically proceed.**

5.  **Session Completion:**
    After the final survey (following the DDA round), the experiment is complete. The application will automatically return to the main lobby. You can now safely close the program. All data has been saved.

## 6. Data Output

The results of the experiment are saved in the `experiment_results.csv` file in the root directory. Each row in this file represents a single participant's experience in one of the four conditions.

The columns are defined as follows:

| Column Name       | Type    | Description                                                                 |
|-------------------|---------|-----------------------------------------------------------------------------|
| `Timestamp`       | String  | The date and time the session was completed.                                |
| `Player_ID`       | String  | A unique identifier (UUID) assigned to each participant for the session.    |
| `Mode_Played`     | String  | The difficulty condition being tested (`EASY`, `MEDIUM`, `HARD`, or `DDA`).   |
| `Win_Loss`        | String  | The outcome of the mini-game for that condition (`WIN` or `LOSS`).            |
| `Q1_Boredom`      | Integer | The participant's self-reported boredom level (1-5 scale).                  |
| `Q2_Frustration`  | Integer | The participant's self-reported frustration level (1-5 scale).              |
| `Q3_Flow`         | Integer | The participant's self-reported focus/flow state (1-5 scale).               |

This structured output is designed for easy import into statistical analysis software like R, SPSS, or Python libraries such as Pandas and SciPy.

## 7. Data Visualization

After collecting data, you can automatically generate a set of professional, poster-ready graphs by running the `plot_graph.py` script.

**To generate the graphs:**
```bash
python plot_graph.py
```

This will read the `experiment_results.csv` file and produce the following three images inside the `Graph/` directory:

*   `Graph/graph_flow.png`: A bar chart showing the average "Flow" score for each of the four difficulty modes.
*   `Graph/graph_emotion.png`: A grouped bar chart comparing the average "Boredom" and "Frustration" scores side-by-side for each mode.
*   `Graph/graph_winrate.png`: A bar chart showing the win rate percentage for each mode.
