"""
board.py

This module defines the `SudokuBoard` class, which represents a 9×9 Sudoku puzzle.

It is responsible for managing the board state and providing utility methods for
accessing and modifying cells, validating moves, determining candidate values,
and locating the next optimal cell to solve using the Minimum Remaining Values (MRV)
heuristic.

The class is intentionally independent of the solving algorithm, following the
Single Responsibility Principle (SRP). It serves as the core data model used by
the Sudoku solver.

Features:
- Store and manage the Sudoku board
- Validate board dimensions
- Retrieve and update cell values
- Identify empty cells
- Calculate row, column, and 3×3 box values
- Generate valid candidate numbers for each empty cell
- Select the next cell using the MRV heuristic
- Detect whether the puzzle is completely solved

Author: Rojina Karrabi
"""

from __future__ import annotations

from copy import deepcopy
from typing import List, Optional, Set


Board = List[List[int]]


class SudokuBoard:
    """
    Represents a Sudoku board.

    Empty cells are represented by 0.
    """

    SIZE = 9

    def __init__(self, board: Board):

        if len(board) != self.SIZE:
            raise ValueError("Board must contain exactly 9 rows.")

        for row in board:
            if len(row) != self.SIZE:
                raise ValueError("Each row must contain exactly 9 columns.")

        self.board = deepcopy(board)

    ###########################################################

    def copy(self) -> "SudokuBoard":
        return SudokuBoard(self.board)

    ###########################################################

    def get(self, row: int, col: int) -> int:
        return self.board[row][col]

    ###########################################################

    def set(self, row: int, col: int, value: int):

        self.board[row][col] = value

    ###########################################################

    def is_empty(self, row: int, col: int) -> bool:

        return self.board[row][col] == 0

    ###########################################################

    def row_values(self, row: int) -> Set[int]:

        return {n for n in self.board[row] if n != 0}

    ###########################################################

    def column_values(self, col: int) -> Set[int]:

        return {
            self.board[r][col]
            for r in range(self.SIZE)
            if self.board[r][col] != 0
        }

    ###########################################################

    def box_values(self, row: int, col: int) -> Set[int]:

        values = set()

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):

                value = self.board[r][c]

                if value != 0:
                    values.add(value)

        return values

    ###########################################################

    def candidates(self, row: int, col: int) -> Set[int]:

        if not self.is_empty(row, col):
            return set()

        used = (
            self.row_values(row)
            | self.column_values(col)
            | self.box_values(row, col)
        )

        return set(range(1, 10)) - used

    ###########################################################

    def find_best_cell(self) -> Optional[tuple[int, int]]:

        """
        MRV heuristic.
        Return the empty cell with the fewest candidates.
        """

        best = None
        minimum = 10

        for r in range(self.SIZE):

            for c in range(self.SIZE):

                if self.is_empty(r, c):

                    count = len(self.candidates(r, c))

                    if count < minimum:

                        minimum = count
                        best = (r, c)

        return best

    ###########################################################

    def solved(self) -> bool:

        return all(
            self.board[r][c] != 0
            for r in range(self.SIZE)
            for c in range(self.SIZE)
        )

    ###########################################################

    def __str__(self):

        lines = []

        for r, row in enumerate(self.board):

            if r and r % 3 == 0:
                lines.append("-" * 21)

            line = []

            for c, value in enumerate(row):

                if c and c % 3 == 0:
                    line.append("|")

                line.append(str(value) if value else ".")

            lines.append(" ".join(line))

        return "\n".join(lines)
