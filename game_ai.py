import numpy as np
from game_functions import GameBoard

class GameAI:
    def __init__(self, search_multiplier=10, length_multiplier=4, search_interval=200):
        self.search_multiplier = search_multiplier
        self.length_multiplier = length_multiplier
        self.search_interval = search_interval

    def _calculate_search_depth(self, move_count):
        simulations = self.search_multiplier * (1 + (move_count // self.search_interval))
        depth = self.length_multiplier * (1 + (move_count // self.search_interval))
        return simulations, depth
        
        
        