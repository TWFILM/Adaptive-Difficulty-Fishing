import pygame
import math
import time
import csv

# --- Configuration ---
WIDTH, HEIGHT = 400, 600
BG_COLOR = (20, 30, 40)       # Deep ocean blue background
BAR_COLOR = (100, 255, 100)   # Green (Player's Bar)
FISH_COLOR = (255, 80, 80)    # Red (The Fish)

# --- DDA Variables ---
difficulty_score = 1.0        # Base difficulty
player_bar_height = 100       # Initial bar height (Reduced from 150)
fish_speed_mult = 1.0         # Fish speed multiplier

# Data logging for research analysis
research_data = []
start_time = time.time()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stardew DDA Experiment")
    clock = pygame.time.Clock()
    
    # Initial positions
    player_y = HEIGHT // 2
    fish_y = HEIGHT // 2
    
    # Player bar movement speed
    player_velocity = 8 
    
    time_counter = 0
    global difficulty_score, player_bar_height, fish_speed_mult

    running = True
    while running:
        # 1. Check Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Player Control (Arrow Keys Up/Down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= player_velocity
        if keys[pygame.K_DOWN]:
            player_y += player_velocity

        # Boundary checks for player bar
        if player_y < 0: player_y = 0
        if player_y > HEIGHT - player_bar_height: player_y = HEIGHT - player_bar_height

        # 3. Fish Behavior Logic (Procedural Animation)
        # Increase time counter based on speed multiplier (DDA)
        time_counter += 0.05 * fish_speed_mult
        
        # Fish movement formula: Primary Sine Wave + Secondary Sine Wave (for unpredictability)
        fish_offset = (math.sin(time_counter) * 150) + (math.sin(time_counter * 3) * 50)
        fish_y = (HEIGHT // 2) + fish_offset
        
        # Boundary checks for fish
        fish_size = 20 # Fixed fish size
        if fish_y < 0: fish_y = 0
        if fish_y > HEIGHT - fish_size: fish_y = HEIGHT - fish_size

        # 4. Collision Detection (Is the fish inside the bar?)
        fish_center = fish_y + (fish_size / 2)
        bar_top = player_y
        bar_bottom = player_y + player_bar_height
        
        is_catching = (fish_center > bar_top) and (fish_center < bar_bottom)

        # --- THE CORE DDA LOGIC (Research Focus) ---
        if is_catching:
            # Condition: Player is performing well (Catching)
            # Action: Increase difficulty
            
            difficulty_score += 0.002
            
            # Decrease bar size (Harder), limit minimum size to 40px
            player_bar_height = max(40, player_bar_height - 0.2)
            
            # Increase fish speed slightly, limit max speed to 3.0x
            fish_speed_mult = min(3.0, fish_speed_mult + 0.001)
            
            status_color = (0, 255, 0) # Green indicator
        else:
            # Condition: Player is failing (Missing)
            # Action: Decrease difficulty (Assist mode)
            
            difficulty_score = max(0.5, difficulty_score - 0.01) # Drop difficulty faster than raising it
            
            # Increase bar size (Easier), limit max size to 250px
            player_bar_height = min(250, player_bar_height + 1.0) 
            
            # Decrease fish speed
            fish_speed_mult = max(0.5, fish_speed_mult - 0.005)
            
            status_color = (255, 0, 0) # Red indicator

        # 5. Data Logging
        current_t = round(time.time() - start_time, 2)
        # Schema: [Time, Bar_Height(Variable), Fish_Speed(Variable), Catch_Status(Binary)]
        research_data.append([current_t, round(player_bar_height, 2), round(fish_speed_mult, 3), int(is_catching)])

        # 6. Rendering
        screen.fill(BG_COLOR)
        
        # Draw Background Track (Visual Guide)
        pygame.draw.rect(screen, (30, 45, 60), (WIDTH//2 - 25, 0, 50, HEIGHT))

        # Draw Player Bar (Green)
        pygame.draw.rect(screen, BAR_COLOR, (WIDTH//2 - 25, int(player_y), 50, int(player_bar_height)))
        
        # Draw Fish (Red)
        pygame.draw.rect(screen, FISH_COLOR, (WIDTH//2 - 15, int(fish_y), 30, int(fish_size)))
        
        # Draw Status Indicator
        pygame.draw.circle(screen, status_color, (WIDTH - 30, 30), 10)

        # Display Real-time Metrics on Screen
        font = pygame.font.SysFont("Arial", 20)
        info_text = [
            f"Time: {current_t}s",
            f"Bar Height: {int(player_bar_height)}px (DDA)",
            f"Fish Speed: {fish_speed_mult:.2f}x (DDA)",
            f"Catching: {'YES' if is_catching else 'NO'}"
        ]
        
        for i, line in enumerate(info_text):
            img = font.render(line, True, (200, 200, 200))
            screen.blit(img, (10, 10 + i*25))

        pygame.display.flip()
        clock.tick(60)

    # End of Experiment: Export Data to CSV
    with open('dda_result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Bar_Height", "Fish_Speed", "Is_Catching"])
        writer.writerows(research_data)
    
    print("Experiment finished. Data saved to 'dda_result.csv'.")
    pygame.quit()

if __name__ == "__main__":
    main()
