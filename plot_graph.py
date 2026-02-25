# plot_graph.py
#
# This script reads the final research data from `experiment_results.csv`
# and generates three professional, poster-ready visualizations for analysis.
# It is designed to be run after data collection is complete.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Configuration ---
INPUT_CSV = 'experiment_results.csv'
OUTPUT_DIR = 'Graph'
OUTPUT_FLOW_GRAPH = os.path.join(OUTPUT_DIR, 'graph_flow.png')
OUTPUT_EMOTION_GRAPH = os.path.join(OUTPUT_DIR, 'graph_emotion.png')
OUTPUT_WINRATE_GRAPH = os.path.join(OUTPUT_DIR, 'graph_winrate.png')

# Define a consistent order for the difficulty modes on the X-axis
MODE_ORDER = ['EASY', 'MEDIUM', 'HARD', 'DDA']

def plot_flow_state(df):
    """Generates and saves a bar chart for average Flow State scores."""
    print("Generating Flow State graph...")
    
    # Calculate average flow score for each mode
    avg_flow = df.groupby('Mode_Played')['Q3_Flow'].mean().reindex(MODE_ORDER)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.bar(avg_flow.index, avg_flow.values, color=['#4E79A7', '#F28E2B', '#E15759', '#76B7B2'])
    
    ax.set_title('Average Reported Flow State per Difficulty Mode', fontsize=16, pad=20)
    ax.set_ylabel('Average Flow Score (1-5)', fontsize=12)
    ax.set_xlabel('Difficulty Mode', fontsize=12)
    ax.set_ylim(0, 5.5)
    ax.grid(axis='x') # Keep vertical grid lines only

    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(OUTPUT_FLOW_GRAPH, dpi=300)
    plt.close()
    print(f"  -> Saved '{OUTPUT_FLOW_GRAPH}'")


def plot_boredom_frustration(df):
    """Generates and saves a grouped bar chart for boredom and frustration."""
    print("Generating Boredom vs. Frustration graph...")

    # Group by mode and calculate means
    emotion_means = df.groupby('Mode_Played')[['Q1_Boredom', 'Q2_Frustration']].mean().reindex(MODE_ORDER)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(emotion_means.index))  # the label locations
    width = 0.35  # the width of the bars

    rects1 = ax.bar(x - width/2, emotion_means['Q1_Boredom'], width, label='Boredom', color='#5975A4')
    rects2 = ax.bar(x + width/2, emotion_means['Q2_Frustration'], width, label='Frustration', color='#CC8963')

    ax.set_title('Average Boredom and Frustration by Mode', fontsize=16, pad=20)
    ax.set_ylabel('Average Score (1-5)', fontsize=12)
    ax.set_xlabel('Difficulty Mode', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(emotion_means.index)
    ax.set_ylim(0, 5.5)
    ax.legend()
    ax.grid(axis='x')

    # Attach a text label above each bar
    ax.bar_label(rects1, padding=3, fmt='%.2f')
    ax.bar_label(rects2, padding=3, fmt='%.2f')

    fig.tight_layout()
    plt.savefig(OUTPUT_EMOTION_GRAPH, dpi=300)
    plt.close()
    print(f"  -> Saved '{OUTPUT_EMOTION_GRAPH}'")


def plot_win_rate(df):
    """Generates and saves a bar chart for the win rate percentage per mode."""
    print("Generating Win Rate graph...")

    # Calculate win rate
    win_rate = df[df['Win_Loss'] == 'WIN'].groupby('Mode_Played').size()
    total = df.groupby('Mode_Played').size()
    win_percentage = (win_rate / total * 100).fillna(0).reindex(MODE_ORDER)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.bar(win_percentage.index, win_percentage.values, color=['#4E79A7', '#F28E2B', '#E15759', '#76B7B2'])

    ax.set_title('Win Rate Percentage per Difficulty Mode', fontsize=16, pad=20)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_xlabel('Difficulty Mode', fontsize=12)
    ax.set_ylim(0, 110)
    ax.grid(axis='x')

    # Add value labels
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(OUTPUT_WINRATE_GRAPH, dpi=300)
    plt.close()
    print(f"  -> Saved '{OUTPUT_WINRATE_GRAPH}'")


def main():
    """Main function to load data and generate all plots."""
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Attempting to read data from '{INPUT_CSV}'...")
    try:
        df = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"Error: '{INPUT_CSV}' not found.")
        print("Please ensure you have run the experiment and the results file exists.")
        return

    # --- Data Cleaning ---
    # Drop rows with missing survey data as they cannot be plotted
    initial_rows = len(df)
    df.dropna(subset=['Q1_Boredom', 'Q2_Frustration', 'Q3_Flow'], inplace=True)
    if len(df) < initial_rows:
        print(f"Dropped {initial_rows - len(df)} rows with missing survey data.")

    # Ensure Mode_Played is a categorical type with the correct order for plotting
    df['Mode_Played'] = pd.Categorical(df['Mode_Played'], categories=MODE_ORDER, ordered=True)
    
    # Generate all three plots
    plot_flow_state(df.copy())
    plot_boredom_frustration(df.copy())
    plot_win_rate(df.copy())
    
    print(f"\nAll graphs generated successfully in '{OUTPUT_DIR}/' directory.")


if __name__ == "__main__":
    main()
