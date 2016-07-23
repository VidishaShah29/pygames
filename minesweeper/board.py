# -*- coding: utf-8 -*-

import numpy as np

class Board(object):
    """
    Represents the board of Minesweeper game. Internally there are three Numpy 2D arrays (matrices).
    First represents the real board, second what can be seen and third the flags.
    Mines are randomly placed after first tile is clicked and not in it's surrounding. Then are
    calculated the mine counts.

    Gaming matrix values:
        0 - clear
        1:8 - no. of mines around
        9 - mine

    Visible matrix values:
        True - visible tile
        False - not visible tile

    Flag matrix values:
        True - flag on tile
        False - no flag on tile
    """

    CLEAR = 0
    MINE = 9

    def __init__(self, width:int, height:int, n_mines:int):
        """
        :param width: no. of cols
        :param height: no. of rows
        :param n_mines: no. of mines
        """

        self.__visibility_matrix = np.zeros((height, width), dtype=bool)
        self.__matrix = np.zeros((height, width), dtype=np.int32)
        self.__flag_matrix = np.copy(self.__visibility_matrix)
        self.__initialized = False
        self.__n_mines = n_mines

    @property
    def visibility_matrix(self) -> np.ndarray:
        """
        :return: the matrix of what is visible
        """

        return self.__visibility_matrix

    @visibility_matrix.setter
    def visibility_matrix(self, matrix:np.ndarray):
        """
        Set the visibility matrix.
        """

        self.__visibility_matrix = matrix

    @property
    def matrix(self) -> np.ndarray:
        """
        :return: the gaming matrix
        """

        return self.__matrix

    @matrix.setter
    def matrix(self, matrix:np.ndarray):
        """
        Set the gaming matrix.
        """

        self.__matrix = matrix
        self.__n_mines = len(matrix[matrix == self.MINE])

    @property
    def flag_matrix(self) -> np.ndarray:
        """
        :return: the flag matrix
        """

        return self.__flag_matrix

    @flag_matrix.setter
    def flag_matrix(self, matrix:np.ndarray):
        """
        Set the flag matrix.
        """

        self.flag_matrix = matrix

    @property
    def initialized(self) -> bool:
        """
        :return: True if matrix is initialized (first tile was clicked), False otherwise.
        """

        return self.__initialized

    @initialized.setter
    def initialized(self, value:bool):
        """
        Set the initialization status.

        :param value:
        """

        self.__initialized = value

    @property
    def shape(self) -> tuple:
        """
        :return: Tuple of the gaming board shape, i.e. the Numpy 2D array dimensions -> (rows, columns)
        """

        return self.matrix.shape

    @property
    def n_mines(self) -> int:
        """
        :return: Number of mines on the board.
        """

        return self.__n_mines

    class GameOverException(Exception):
        pass

    class GameFinishedException(Exception):
        pass

    def __get_surrounding_tiles_indexes(self, row:int, col:int) -> list:
        """
        :param row:
        :param col:
        :return: list of indexes of the surrounding tiles
        """

        all_indexes = [(row-1, col-1), (row-1, col), (row-1, col+1),
                       (row, col-1),                 (row, col+1),
                       (row+1, col-1), (row+1, col), (row+1, col+1)]
        indexes = []

        for i in all_indexes:
            if 0 <= i[0] < self.shape[0] and 0 <= i[1] < self.shape[1]:
                indexes.append(i)

        return indexes

    def __init_board(self, row:int, col:int):
        """
        Randomly place n mines on the gaming board, but somewhere else than in the
        surrounding of the first clicked tile.

        :param row:
        :param col:
        :param n_mines:
        """

        n_placed_mines = 0
        row_range = np.arange(0, self.shape[0])
        col_range = np.arange(0, self.shape[1])
        surrounding_indexes = self.__get_surrounding_tiles_indexes(row, col)

        # randomly place mines, but not in the surrounding of the first clicked tile
        while n_placed_mines != self.n_mines:
            index = (np.random.choice(row_range, 1)[0], np.random.choice(col_range, 1)[0])
            if index not in surrounding_indexes and index != (row, col) and self.matrix[index] != self.MINE:
                self.matrix[index] = self.MINE
                n_placed_mines += 1

        # count mines
        for i in row_range:
            for j in col_range:
                if self.matrix[i, j] != self.MINE:
                    surrounding_indexes = self.__get_surrounding_tiles_indexes(i, j)
                    # rebuild to [[rows indexes], [col indexes]]
                    surrounding_indexes = [[x[0] for x in surrounding_indexes],
                                           [x[1] for x in surrounding_indexes]]
                    self.matrix[i, j] = np.count_nonzero(
                        self.matrix[surrounding_indexes[0], surrounding_indexes[1]] == self.MINE)

        self.__initialized = True

    def __uncover(self, row:int, col:int):
        """
        Recursively uncover the zero tiles and tiles with mine's count, which are next to them.

        :param row:
        :param col:
        """

        surrounding_indexes = self.__get_surrounding_tiles_indexes(row, col)
        clear_tile = self.matrix[row, col] == self.CLEAR
        self.visibility_matrix[row, col] = True

        for i in surrounding_indexes:
            # TODO: If clicked tile is a mine's count, should I also uncover the surrounding clear tiles?
            # if (self.matrix[i] in range(1, 9) and clear_tile) or self.matrix[i] == self.CLEAR:
            if self.matrix[i] in range(1, 9) and clear_tile:
                self.visibility_matrix[i] = True
            elif clear_tile:
                if not self.visibility_matrix[i]:
                    self.visibility_matrix[i] = True
                    self.__uncover(i[0], i[1])

    def __check_game_finish(self) -> bool:
        """
        Check if the game is finished (won), i.e. only tiles with mines are uncovered.

        :return: True if game is finished (won), False otherwise.
        """

        return len(self.visibility_matrix[self.visibility_matrix == False]) == self.n_mines

    def click(self, row:int, col:int) -> bool:
        """
        Click the tile on the gaming matrix.

        :param row:
        :param col:
        :return: True if click was succesfully performed, False otherwise (e.g. click on the revealed tile).
        """

        if self.matrix[row, col] == self.MINE:
            raise self.GameOverException("Game over! You clicked on the mine!")

        if self.visibility_matrix[row, col]:
            return False

        if not self.initialized:
            self.__init_board(row, col)

        self.__uncover(row, col)

        if self.__check_game_finish():
            raise self.GameFinishedException("Congratulation, you win!")

        return True

    def place_flag(self, row:int, col:int) -> bool:
        """
        Place a flag on the mine-suspicious tile (i.e. internally change value to 11).

        :param row:
        :param col:
        :return: True if flag was succesfully placed (tile must be not visible), False otherwise.
        """

        if not self.visibility_matrix[row, col]:
            self.flag_matrix[row, col] = True
            return True
        else:
            return False

    def remove_flag(self, row:int, col:int) -> bool:
        """
        Remove the flag from tile.

        :param row:
        :param col:
        :return: True if flag was succesfully removed, False otherwise (i.e. there is no flag on this tile).
        """

        if self.flag_matrix[row, col]:
            self.flag_matrix[row, col] = False
            return True
        else:
            return False

    def get_mines_indexes(self) -> list:
        """
        :return: List of indexes of tiles with mines.
        """

        indexes = np.where(self.matrix == self.MINE)
        return list(zip(indexes[0], indexes[1]))

    def pretty_output(self, special_chars=False, as_string=False) -> np.ndarray:
        """
        Output gaming board.

        :return:
        """

        to_string = np.vectorize(str)

        pretty_matrix = np.ma.masked_where(~self.visibility_matrix, self.matrix)
        pretty_matrix = to_string(pretty_matrix)
        pretty_matrix = pretty_matrix.filled("?")

        if as_string and not special_chars:
            pretty_matrix_str = ""

            for i in range(0, self.shape[0]):
                for j in range(0, self.shape[1]):
                    pretty_matrix_str += pretty_matrix[i, j]
                    if j != self.shape[1] - 1:
                        pretty_matrix_str += " "
                pretty_matrix_str += "\n"
            return pretty_matrix_str

        if special_chars:
            ascii_dict = {
                "?": "?",
                "0": "▒"
            }

            pretty_matrix = np.vectorize(lambda x: ascii_dict[x] if x in ascii_dict.keys() else x)(pretty_matrix)

            if not as_string:
                return pretty_matrix

            corner_dict = {
                "topleft": "╔",
                "topright": "╗",
                "bottomleft": "╚",
                "bottomright": "╝",
            }
            hor_border = "═"
            ver_border = "║"

            if self.shape[1] % 2:
                hor_border_multiplier = self.shape[1] + 2
            else:
                hor_border_multiplier = self.shape[1] + 1

            pretty_matrix_str = "{topleft}{hor_border}{topright}\n".format(
                topleft=corner_dict["topleft"],
                hor_border="".join([hor_border] * hor_border_multiplier),
                topright=corner_dict["topright"]
            )

            for i in range(0, self.shape[0]):
                pretty_matrix_str += ver_border
                for j in range(0, self.shape[1]):
                    pretty_matrix_str += pretty_matrix[i, j]
                    if j != self.shape[1] - 1:
                        pretty_matrix_str += " "
                pretty_matrix_str += ver_border
                pretty_matrix_str += "\n"

            pretty_matrix_str += "{bottomleft}{hor_border}{bottomright}\n".format(
                bottomleft=corner_dict["bottomleft"],
                hor_border="".join([hor_border] * hor_border_multiplier),
                bottomright=corner_dict["bottomright"]
            )

            return pretty_matrix_str