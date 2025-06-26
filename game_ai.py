import numpy as np
import random

class GameAI:
    def __init__(self, search_depth_factor=10, move_depth_factor=4, depth_increment_interval=200):
        self.search_depth_factor = search_depth_factor
        self.move_depth_factor = move_depth_factor
        self.depth_increment_interval = depth_increment_interval

    def calculate_search_parameters(self, move_count):
        simulations = self.search_depth_factor * (1 + (move_count // self.depth_increment_interval))
        depth = self.move_depth_factor * (1 + (move_count // self.depth_increment_interval))
        return simulations, depth

    def determine_best_move(self, game_instance):
        return self.monte_carlo_search_strategy(game_instance)

    def monte_carlo_search_strategy(self, game_instance):
        simulations_count, search_depth = 100, 3
        move_evaluations = np.zeros(4)
        current_board = game_instance.get_board()
        
        for direction_index in range(4):
            test_board = np.copy(current_board)
            test_board, move_valid = self.simulate_move(test_board, direction_index)
            
            if not move_valid:
                move_evaluations[direction_index] = -1
                continue
                
            move_evaluations[direction_index] += self.evaluate_board_state(test_board)
            
            for simulation_index in range(simulations_count):
                simulation_board = np.copy(test_board)
                for depth_step in range(search_depth):
                    if not self.perform_random_move(simulation_board):
                        break
                move_evaluations[direction_index] += self.evaluate_board_state(simulation_board)
                
        return int(np.argmax(move_evaluations))

    def simulate_move(self, board_state, direction_code):
        rotation_mapping = {0: 2, 1: -1, 2: 0, 3: 1}
        rotated_board = np.rot90(board_state, rotation_mapping[direction_code])
        slid_board, slide_changed = self.slide_tiles_right(rotated_board)
        merged_board, slide_changed, slide_changed = self.merge_tiles(slid_board)
        result_board, slide_changed = self.slide_tiles_right(merged_board)
        final_board = np.rot90(result_board, -rotation_mapping[direction_code])
        return final_board, not np.array_equal(board_state, final_board)

    def perform_random_move(self, board_state):
        valid_moves = []
        for direction in range(4):
            slide_changed, move_valid = self.simulate_move(board_state, direction)
            if move_valid:
                valid_moves.append(direction)
        
        if not valid_moves:
            return False
            
        chosen_direction = random.choice(valid_moves)
        board_state[:], slide_changed = self.simulate_move(board_state, chosen_direction)
        return True

    def evaluate_board_state(self, board_state):
        return np.sum(board_state) + np.count_nonzero(board_state) * 10

    def slide_tiles_right(self, board_state):
        grid_dimension = board_state.shape[0]
        result_board = np.zeros_like(board_state)
        change_flag = False
        for row_index in range(grid_dimension):
            insert_position = grid_dimension - 1
            for column_index in reversed(range(grid_dimension)):
                if board_state[row_index][column_index] != 0:
                    result_board[row_index][insert_position] = board_state[row_index][column_index]
                    if column_index != insert_position:
                        change_flag = True
                    insert_position -= 1
        return result_board, change_flag

    def merge_tiles(self, board_state):
        grid_dimension = board_state.shape[0]
        merge_score = 0
        merge_flag = False
        for row_index in range(grid_dimension):
            for column_index in reversed(range(1, grid_dimension)):
                current_value = board_state[row_index][column_index]
                left_value = board_state[row_index][column_index - 1]
                if current_value == left_value and current_value != 0:
                    board_state[row_index][column_index] *= 2
                    merge_score += board_state[row_index][column_index]
                    board_state[row_index][column_index - 1] = 0
                    merge_flag = True
        return board_state, merge_flag, merge_score