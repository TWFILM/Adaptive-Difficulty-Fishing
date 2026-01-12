import json
from pathlib import Path
import random

def get_fish(rarity):
    fish_data = {}
    path = Path(__file__).parent / "fish_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        fish_data = json.load(f)

    return random.choice(fish_data[rarity])

def get_random_rarity(rod_name):
    rod = get_fishing_rod_info(rod_name)
    rarities = ["common", "uncommon", "rare", "legendary", "Mythical"]
    weights = [1/2, 1/4, 1/8, 1/16, 1/32]

    luck = rod.get("LUCK", 0)
    if luck!=0:
        if luck < 0:
            weights[0] = weights[0] * 1+abs(luck) # common
        else :
            weights[0] = weights[0] * abs(luck)/2 # common
        weights[1] *= 1+luck # uncommon
        weights[2] *= 1+(luck*2) # rare
        weights[3] *= 1+(luck*4) # legendary
        weights[4] *= 1+(luck*8) # mythical
           
    
    result = random.choices(rarities, weights=weights, k=1)
    print(weights)
    return result[0]

def get_fishing_rod_info(name):
    rod_data = {}
    path = Path(__file__).parent / "fishing_rod_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        rod_data = json.load(f)

    return rod_data[name]