from board import Board
import numpy as np

board = Board(4, 4, max_random_value=4)

board.matrix = np.array(
    [[4, 2, 0, 2, 0],
    [0, 2, 0, 0, 0],
    [4, 0, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [4, 8, 0, 0, 0]]
)


board.matrix = np.array(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
)

print(board.matrix)
board.move("up")
board.insert_random_tile()
print()
print(board.matrix)