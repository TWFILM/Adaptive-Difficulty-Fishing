# dda.py
def update_fish_speed(is_catching, fish_speed):
    if is_catching:
        return min(3.0, fish_speed + 0.001)
    else:
        return max(0.5, fish_speed - 0.005)
