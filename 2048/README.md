# 2048 game

original: https://gabrielecirulli.github.io/2048/

## Motivation

Generally I made this 2048 'backend' to try some solving algorithms. The most I want to try some neural network (deep learning).

## `board.py`

The `board.py` contains the `Board` class, which behaves as a board for a 2048 game. Internally it's a Numpy 2D array (matrix).
The inner behaviour of board is documented in function's docstrings.

`Board` constructor: `Board(width, height, max_random_value=4)`

`max_random_value` means (as the name suggests) which maximum value can a random tile (which is added after every successful move
or on the game start) have.

`max_random_value=4` is for values 2 and 4

`max_random_value=16` for values 2, 4, 8, 16

## `2048_game.py`

The `2048_game.py` is just a very simple 'rendering' of the 2048 board, with keyboard arrows moving.

### Dependencies

`Python 3.5.1`

I have used these versions of libraries, but other versions should work too:

`mkl 11.3.3`

`numpy 1.11.1`

`pygame 1.9.2a0`

I am using the **conda** package manager and it's great: http://conda.pydata.org/docs/

You can download `pygame` for Python 3.5 here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

Then just install it with `pip install <pygame file>`
