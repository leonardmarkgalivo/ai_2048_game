import numpy as np

class GameLogic:
    def __init__(self):
        self.tile_distribution = [2]*9 + [4]
        self.grid_size = 4
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self._add_initial_tiles()

    def _add_initial_tiles(self):
        for _ in range(2):
            self.board = self._add_new_tile(self.board)

    def _add_new_tile(self, board):
        empty_cells = list(zip(*np.where(board == 0)))
        if empty_cells:
            chosen_tile = np.random.choice(self.tile_distribution)
            selected_index = np.random.choice(len(empty_cells))
            row, col = empty_cells[selected_index]
            board[row][col] = chosen_tile
        return board

        

