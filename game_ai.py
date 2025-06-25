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

    def choose_move(self, board_instance, simulations, depth):
        move_scores = np.zeros(4)
        for direction_index in range(4):
            test_instance = GameBoard()
            test_instance.board = np.copy(board_instance.board)
            move_successful, score = test_instance.move(direction_index)
            if not move_successful:
                continue
            move_scores[direction_index] += score
            for _ in range(simulations):
                simulated_instance = GameBoard()
                simulated_instance.board = np.copy(test_instance.board)
                for _ in range(depth):
                    random_direction = np.random.randint(0, 4)
                    moved, gained = simulated_instance.move(random_direction)
                    if not moved:
                        break
                    move_scores[direction_index] += gained
        best_direction = int(np.argmax(move_scores))
        return best_direction

    def automated_play(self):
        current_game = GameBoard()
        game_active = True
        total_moves = 0
        while game_active:
            total_moves += 1
            sim_count, search_len = self._calculate_search_depth(total_moves)
            direction = self.choose_move(current_game, sim_count, search_len)
            moved, _ = current_game.move(direction)
            if not moved or current_game.is_game_over() or current_game.is_win():
                game_active = False
            print(current_game.board)
        return np.amax(current_game.board)
