# Import tkinter and game_board
# Define Display class inheriting from Frame

# Constructor:
#   - Set up window title
#   - Initialize GameBoard object
#   - Build GUI grid
#   - Update tiles
#   - Bind keyboard events

# Function to build 4x4 grid using Frame and Label widgets

# Function to update grid from the GameBoard state:
#   - For each tile:
#     - If zero, show empty cell
#     - Else, show value with color

# Key handler function:
#   - Map keys 'w', 'a', 's', 'd' to directions
#   - Call GameBoard move method
#   - If moved, update the grid
#   - If 2048 reached, print win
#   - If no moves left, print game over
