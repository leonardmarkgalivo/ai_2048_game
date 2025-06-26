from tkinter import Frame, Label, CENTER
from game_functions import Game2048
from game_ai import GameAI

EDGE_LENGTH = 400
CELL_COUNT = 4
CELL_PAD = 10

UP_KEY = 'w'
DOWN_KEY = 's'
LEFT_KEY = 'a'
RIGHT_KEY = 'd'
AI_KEY = 'q'
AI_PLAY_KEY = 'p'

LABEL_FONT = ("Verdana", 40, "bold")
GAME_COLOR = "#a6bdbb"
EMPTY_COLOR = "#8eaba8"

TILE_COLORS = {
    2: "#daeddf", 4: "#9ae3ae", 8: "#6ce68d", 16: "#42ed71",
    32: "#17e650", 64: "#17c246", 128: "#149938", 256: "#107d2e",
    512: "#0e6325", 1024: "#0b4a1c", 2048: "#031f0a", 4096: "#000000", 8192: "#000000"
}

LABEL_COLORS = {
    2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
    32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
    256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
    2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0"
}

class Display(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.handle_key_press)

        self.key_to_direction = {
            UP_KEY: 0,
            RIGHT_KEY: 1,
            DOWN_KEY: 2,
            LEFT_KEY: 3
        }

        self.grid_cells = []
        self.game = Game2048()
        self.ai_controller = GameAI()

        self.initialize_grid()
        self.update_grid_display()
        self.mainloop()

    def initialize_grid(self):
        background_frame = Frame(self, bg=GAME_COLOR, width=EDGE_LENGTH, height=EDGE_LENGTH)
        background_frame.grid()

        for row_index in range(CELL_COUNT):
            row_cells = []
            for column_index in range(CELL_COUNT):
                cell_frame = Frame(
                    background_frame,
                    bg=EMPTY_COLOR,
                    width=EDGE_LENGTH / CELL_COUNT,
                    height=EDGE_LENGTH / CELL_COUNT
                )
                cell_frame.grid(
                    row=row_index,
                    column=column_index,
                    padx=CELL_PAD,
                    pady=CELL_PAD
                )
                tile_label = Label(
                    master=cell_frame,
                    text="",
                    bg=EMPTY_COLOR,
                    justify=CENTER,
                    font=LABEL_FONT,
                    width=5,
                    height=2
                )
                tile_label.grid()
                row_cells.append(tile_label)
            self.grid_cells.append(row_cells)

    def update_grid_display(self):
        current_board = self.game.get_board()
        for row_index in range(CELL_COUNT):
            for column_index in range(CELL_COUNT):
                tile_value = current_board[row_index][column_index]
                cell_widget = self.grid_cells[row_index][column_index]
                if tile_value == 0:
                    cell_widget.configure(text="", bg=EMPTY_COLOR)
                else:
                    cell_widget.configure(
                        text=str(tile_value),
                        bg=TILE_COLORS.get(tile_value, EMPTY_COLOR),
                        fg=LABEL_COLORS.get(tile_value, "#011c08")
                    )
        self.update_idletasks()

    def handle_key_press(self, event):
        pressed_key = event.char
        
        if pressed_key == AI_KEY:
            move_direction = self.ai_controller.determine_best_move(self.game)
            self.game.execute_move(move_direction)
            self.update_grid_display()
            
        elif pressed_key == AI_PLAY_KEY:
            self.run_ai_playback()
            
        elif pressed_key in self.key_to_direction:
            move_direction = self.key_to_direction[pressed_key]
            self.game.execute_move(move_direction)
            self.update_grid_display()
    
    def run_ai_playback(self):
        while True:
            move_direction = self.ai_controller.determine_best_move(self.game)
            if not self.game.execute_move(move_direction):
                break
            self.update_grid_display()
            self.update()
            self.after(100)
            
            if self.game.check_game_over() or self.game.check_win_condition():
                break

if __name__ == "__main__":
    Display()