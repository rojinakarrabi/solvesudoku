"""
solver.py

Sudoku Solver using
- Recursive Backtracking
- MRV (Minimum Remaining Values)

Author: Rojina Karrabi
"""

from board import SudokuBoard


class SudokuSolver:
    """
    Sudoku solving engine.
    """

    def __init__(self, board: SudokuBoard):

        self.board = board

        self.steps = 0

    ########################################################

    def solve(self) -> bool:
        """
        Solve sudoku.

        Returns
        -------
        bool
            True if solved.
        """

        location = self.board.find_best_cell()

        # No empty cells -> solved
        if location is None:
            return True

        row, col = location

        candidates = sorted(self.board.candidates(row, col))

        for value in candidates:

            if self.is_valid(row, col, value):

                self.board.set(row, col, value)

                self.steps += 1

                if self.solve():
                    return True

                # Backtrack
                self.board.set(row, col, 0)

        return False

    ########################################################

    def is_valid(
        self,
        row: int,
        col: int,
        value: int,
    ) -> bool:
        """
        Checks whether placing value is legal.
        """

        return value in self.board.candidates(row, col)

    ########################################################

    def statistics(self):

        return {
            "steps": self.steps,
        }
