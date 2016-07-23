# Minesweeper class

## Motivation

Generally I made this Minesweeper 'backend' to try some solving algorithms. The most I want to try some neural network (deep learning).

## `board.py`

The `board.py` contains the `Board` class, which behaves as a board for a Minesweeper game.
Internally there are three Numpy 2D arrays (matrices):
  - the matrix with mines and tiles with their count
  - the boolean matrix of visibility
  - the boolean matrix of flags

The inner behaviour of board is documented in function's docstrings. The board is init after first 'click' is performed.
This prevents that first 'click' will be on mine. Also all surrounding tiles are omitted to contain mine.

`Board` constructor: `Board(width, height, n_mines)`

### Dependencies

`Python 3.5.1`, but generally Python 3 is probably OK.

I have used these versions of libraries, but other versions should work too:

`mkl 11.3.3`

`numpy 1.11.1`

`pygame 1.9.2a0`

I am using the **conda** package manager and it's great: http://conda.pydata.org/docs/

You can download `pygame` for Python 3.5 here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

Then just install it with `pip install <pygame file>`
