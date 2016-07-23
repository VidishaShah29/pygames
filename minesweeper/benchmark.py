import timeit

setup = """
from board import Board
board = Board(9, 9, 4)
"""

code = """
board.click(1, 1)
"""

print(min(timeit.Timer(code, setup=setup).repeat(7, 10)))