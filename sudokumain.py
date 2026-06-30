"""
main.py

Sudoku Solver CLI

Author:
Rojina Karrabi
"""

import argparse
import json
import time
from pathlib import Path

from board import SudokuBoard
from solver import SudokuSolver


def load_board(path: Path) -> SudokuBoard:
    """
    Load Sudoku board from JSON file.
    """

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return SudokuBoard(data)


def save_board(board: SudokuBoard, path: Path):
    """
    Save solved board to JSON.
    """

    with open(path, "w", encoding="utf-8") as file:
        json.dump(board.board, file, indent=4)


def main():

    parser = argparse.ArgumentParser(
        description="Sudoku Solver"
    )

    parser.add_argument(
        "input",
        help="Input sudoku JSON file"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="solution.json",
        help="Output JSON filename"
    )

    args = parser.parse_args()

    board = load_board(Path(args.input))

    print("\nInitial Board\n")
    print(board)

    solver = SudokuSolver(board)

    start = time.perf_counter()

    solved = solver.solve()

    elapsed = time.perf_counter() - start

    print()

    if solved:

        print("Solved Successfully!\n")

        print(board)

        print()

        print(f"Steps : {solver.steps}")
        print(f"Time  : {elapsed:.5f} sec")

        save_board(board, Path(args.output))

        print(f"\nSolution saved to '{args.output}'")

    else:

        print("No solution exists.")


if __name__ == "__main__":
    main()
