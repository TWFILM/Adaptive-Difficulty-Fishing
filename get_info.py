import json
from pathlib import Path
import random

def get_fish(rarity):
    fish_data = {}
    path = Path(__file__).parent / "fish_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        fish_data = json.load(f)

    return random.choice(fish_data[rarity])

def get_random_rarity():
    rarities = ["common", "uncommon", "rare", "legendary", "Mythical"]
    weights = [1/2, 1/4, 1/8, 1/16, 1/32]
    
    result = random.choices(rarities, weights=weights, k=1)
    return result[0]