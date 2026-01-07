import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_clean_dda():
    # 1. Read file
    try:
        df = pd.read_csv('dda_result.csv')
    except FileNotFoundError:
        print("File not found: dda_result.csv")
        return

    # 2. Setup figure (split into 2 subplots: top and bottom)
    # sharex=True ensures both plots share the same time axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [1, 3]})
    plt.subplots_adjust(hspace=0.1) # Reduce spacing between plots

    # --- Top Plot: Player Status ---
    # Visualize 0/1 as "Catch" vs "Miss" regions for better readability
    ax1.set_title("Player Performance & DDA Response", fontsize=14, fontweight='bold')
    ax1.fill_between(df['Time'], 0, 1, where=df['Is_Catching']==1, color='#90EE90', alpha=0.8, label='Catching (Good)')
    ax1.fill_between(df['Time'], 0, 1, where=df['Is_Catching']==0, color='#FFCCCB', alpha=0.8, label='Missing (Bad)')
    ax1.set_yticks([]) # Hide Y-axis ticks
    ax1.set_ylabel("Player\nState", rotation=0, labelpad=20, fontsize=10, fontweight='bold')
    ax1.legend(loc='upper right', fontsize='small')
    ax1.grid(axis='x', linestyle=':', alpha=0.5)

    # --- Bottom Plot: Game Difficulty ---
    # Plot "Bar Size" but we will invert the axis
    color = 'tab:blue'
    ax2.plot(df['Time'], df['Bar_Height'], color=color, linewidth=2.5)
    
    # *** Important: Invert Y-axis ***
    # Higher values (Larger bar/Easier) at the bottom, Lower values (Smaller bar/Harder) at the top
    # Creates the visual intuition: "Graph going up = Getting Harder"
    ax2.invert_yaxis() 
    
    ax2.set_ylabel("Bar Size (Pixels)\n(Smaller = Harder)", color=color, fontsize=11, fontweight='bold')
    ax2.set_xlabel("Time (Seconds)", fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Add Annotations
    # Highlight the point of maximum difficulty (minimum bar size)
    min_bar = df['Bar_Height'].min()
    min_time = df.loc[df['Bar_Height'].idxmin(), 'Time']
    ax2.annotate(f'Max Difficulty\n(Size: {min_bar:.1f}px)', 
                 xy=(min_time, min_bar), 
                 xytext=(min_time+2, min_bar+10),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=9)

    # --- Save File ---
    output_filename = 'dda_graph.png'
    plt.savefig(output_filename, dpi=100)
    print(f"Graph saved successfully: {output_filename}")

if __name__ == "__main__":
    plot_clean_dda()
