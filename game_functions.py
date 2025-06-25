import numpy as np

class GameBoard:
    def __init__(self):
        self.grid_size = 4
        self.tile_distribution = [2] * 9 + [4]
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self._place_initial_tiles()

    def _place_initial_tiles(self):
        for _ in range(2):
            self.board = self._add_tile(self.board)

    def _add_tile(self, board):
        available_positions = list(zip(*np.where(board == 0)))
        if available_positions:
            new_tile_value = np.random.choice(self.tile_distribution)
            chosen_index = np.random.choice(len(available_positions))
            row_index, col_index = available_positions[chosen_index]
            board[row_index][col_index] = new_tile_value
        return board

    def _slide_right(self, board):
        result_board = np.zeros_like(board)
        has_changed = False
        for row_index in range(self.grid_size):
            insert_position = self.grid_size - 1
            for col_index in reversed(range(self.grid_size)):
                if board[row_index][col_index] != 0:
                    result_board[row_index][insert_position] = board[row_index][col_index]
                    if col_index != insert_position:
                        has_changed = True
                    insert_position -= 1
        return result_board, has_changed

    def _combine_tiles(self, board):
        score_accumulated = 0
        has_combined = False
        for row_index in range(self.grid_size):
            for col_index in reversed(range(1, self.grid_size)):
                current_tile = board[row_index][col_index]
                previous_tile = board[row_index][col_index - 1]
                if current_tile == previous_tile and current_tile != 0:
                    board[row_index][col_index] *= 2
                    score_accumulated += board[row_index][col_index]
                    board[row_index][col_index - 1] = 0
                    has_combined = True
        return board, has_combined, score_accumulated

    def _execute_move_logic(self, board):
        board, shifted = self._slide_right(board)
        board, combined, score = self._combine_tiles(board)
        board, _ = self._slide_right(board)
        return board, (shifted or combined), score

    def move(self, direction_index):
        rotation_steps = {0: 2, 1: -1, 2: 0, 3: 1}
        rotated_board = np.rot90(self.board, rotation_steps[direction_index])
        processed_board, did_move, move_score = self._execute_move_logic(rotated_board)
        self.board = np.rot90(processed_board, -rotation_steps[direction_index])
        if did_move:
            self.board = self._add_tile(self.board)
        return did_move, move_score

    def is_win(self):
        return 2048 in self.board

    def is_game_over(self):
        for direction in range(4):
            test_board = np.copy(self.board)
            rotated = np.rot90(test_board, {0: 2, 1: -1, 2: 0, 3: 1}[direction])
            shifted, _ = self._slide_right(rotated)
            merged, _, _ = self._combine_tiles(shifted)
            if not np.array_equal(rotated, merged):
                return False
        return True