import numpy as np

class Game2048:
    def __init__(self):
        self.grid_size = 4
        self.tile_probabilities = [2] * 9 + [4]
        self.game_board = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.current_score = 0
        self.initialize_game_tiles()
    
    def get_board(self):
        return self.game_board.copy()
    
    def get_score(self):
        return self.current_score

    def initialize_game_tiles(self):
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_positions = list(zip(*np.where(self.game_board == 0)))
        if empty_positions:
            new_tile_value = np.random.choice(self.tile_probabilities)
            position_index = np.random.choice(len(empty_positions))
            row_position, column_position = empty_positions[position_index]
            self.game_board[row_position][column_position] = new_tile_value

    def slide_tiles_right(self, board_state):
        result_board = np.zeros_like(board_state)
        change_occurred = False
        for row_index in range(self.grid_size):
            insert_position = self.grid_size - 1
            for column_index in reversed(range(self.grid_size)):
                if board_state[row_index][column_index] != 0:
                    result_board[row_index][insert_position] = board_state[row_index][column_index]
                    if column_index != insert_position:
                        change_occurred = True
                    insert_position -= 1
        return result_board, change_occurred

    def merge_adjacent_tiles(self, board_state):
        merge_score = 0
        merge_occurred = False
        for row_index in range(self.grid_size):
            for column_index in reversed(range(1, self.grid_size)):
                current_tile = board_state[row_index][column_index]
                adjacent_tile = board_state[row_index][column_index - 1]
                if current_tile == adjacent_tile and current_tile != 0:
                    board_state[row_index][column_index] *= 2
                    merge_score += board_state[row_index][column_index]
                    board_state[row_index][column_index - 1] = 0
                    merge_occurred = True
        return board_state, merge_occurred, merge_score

    def process_move_direction(self, board_state):
        board_after_slide, slide_change = self.slide_tiles_right(board_state)
        board_after_merge, merge_change, move_score = self.merge_adjacent_tiles(board_after_slide)
        board_final, slide_changed = self.slide_tiles_right(board_after_merge)
        return board_final, (slide_change or merge_change), move_score

    def execute_move(self, direction_code):
        rotation_mapping = {0: 2, 1: -1, 2: 0, 3: 1}
        rotated_board = np.rot90(self.game_board, rotation_mapping[direction_code])
        processed_board, move_valid, move_points = self.process_move_direction(rotated_board)
        self.game_board = np.rot90(processed_board, -rotation_mapping[direction_code])
        
        if move_valid:
            self.add_random_tile()
            self.current_score += move_points
        return move_valid

    def check_win_condition(self):
        return 2048 in self.game_board

    def check_game_over(self):
        for direction in range(4):
            test_board = np.copy(self.game_board)
            rotated_board = np.rot90(test_board, {0: 2, 1: -1, 2: 0, 3: 1}[direction])
            slid_board, slide_changed = self.slide_tiles_right(rotated_board)
            merged_board, slide_changed, slide_changed = self.merge_adjacent_tiles(slid_board)
            if not np.array_equal(rotated_board, merged_board):
                return False
        return True