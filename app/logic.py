from typing import List, Optional, Tuple
import json
import random

Board = List[Optional[str]]  # 9 elements: 'X', 'O', or None

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6)              # diagonals
]


# -------------------------------------------------------
# Board Helpers
# -------------------------------------------------------

def _ensure_board(board) -> Board:
    """Accepts a board list or serialized JSON string and always returns a Python list."""
    if isinstance(board, str):
        return json.loads(board)
    return board


def empty_board() -> Board:
    """Returns a fresh empty Tic-Tac-Toe board."""
    return [None] * 9


# -------------------------------------------------------
# Move Handling
# -------------------------------------------------------

def place_mark(board: Board, pos: int, mark: str) -> Board:
    """
    Returns a *new board* with the mark placed.
    Does not mutate the original.
    """
    board = _ensure_board(board)

    if not 0 <= pos <= 8:
        raise ValueError("Position must be between 0 and 8.")
    if board[pos] is not None:
        raise ValueError("Cell already taken.")

    new_board = board.copy()
    new_board[pos] = mark
    return new_board


def valid_move(board: Board, pos: int, player: str) -> Tuple[bool, str]:
    """
    Validates a move:
      - board must not be finished,
      - chosen cell must be empty.
    """
    board = _ensure_board(board)

    if check_winner(board):
        return False, "Game already finished (winner decided)."
    if is_draw(board):
        return False, "Game already finished (draw)."

    if not 0 <= pos <= 8:
        return False, "Invalid position. Must be 0–8."

    if board[pos] is not None:
        return False, "Cell already taken."

    return True, "ok"


# -------------------------------------------------------
# Game Status Checks
# -------------------------------------------------------

def check_winner(board: Board) -> Optional[str]:
    """
    Returns 'X', 'O', or None if there is no winner.
    """
    board = _ensure_board(board)

    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    return None


def is_draw(board: Board) -> bool:
    """
    True if board is full and no winner.
    """
    board = _ensure_board(board)
    return all(cell is not None for cell in board) and check_winner(board) is None


# -------------------------------------------------------
# Computer AI
# -------------------------------------------------------

def compute_computer_move(board: Board) -> Board:
    """
    Computer AI:
      - Blocks X from winning.
      - Finishes winning move if available.
      - Otherwise picks a random empty cell.
    Always returns a *new board*.
    """
    board = _ensure_board(board)
    new_board = board.copy()

    # Try winning → 'O'
    for a, b, c in WIN_LINES:
        line = [new_board[a], new_board[b], new_board[c]]

        # Win if possible
        if line.count("O") == 2 and line.count(None) == 1:
            idx = [a, b, c][line.index(None)]
            new_board[idx] = "O"
            return new_board

    # Try blocking → block 'X'
    for a, b, c in WIN_LINES:
        line = [new_board[a], new_board[b], new_board[c]]

        if line.count("X") == 2 and line.count(None) == 1:
            idx = [a, b, c][line.index(None)]
            new_board[idx] = "O"
            return new_board

    # Pick a random available square
    empty_positions = [i for i, cell in enumerate(new_board) if cell is None]
    if empty_positions:
        choice = random.choice(empty_positions)
        new_board[choice] = "O"

    return new_board
