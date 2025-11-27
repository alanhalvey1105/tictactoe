from app.logic import empty_board, place_mark, check_winner, is_draw
import pytest


def test_win_row():
    board = empty_board()
    board = place_mark(board, 0, "X")
    board = place_mark(board, 1, "X")
    board = place_mark(board, 2, "X")

    assert check_winner(board) == "X"


def test_draw():
    board = [
        "X", "O", "X",
        "X", "O", "O",
        "O", "X", "X",
    ]

    assert is_draw(board)

def test_create_empty_board_has_9_cells():
    board = empty_board()
    assert len(board) == 9
    assert all(cell is None for cell in board)

def test_make_valid_move_updates_board():
    board = empty_board()
    new_board = place_mark(board, 0, "X")
    assert new_board[0] == "X"

@pytest.mark.parametrize(
    "board,expected_winner",
    [
        (["X", "X", "X", None, None, None, None, None, None], "X"),  # row
        ([None, None, None, "O", "O", "O", None, None, None], "O"),
        (["X", None, None, "X", None, None, "X", None, None], "X"),  # column
        (["O", None, None, None, "O", None, None, None, "O"], "O"),
        (["X", None, None, None, "X", None, None, None, "X"], "X"),  # diagonal
        (["O", None, None, None, "O", None, None, None, "O"], "O"),
    ],
)
def test_check_winner_detects_winner(board, expected_winner):
    assert check_winner(board) == expected_winner


def test_check_winner_returns_none_for_ongoing_game():
    board = ["X", "O", "X", None, "O", None, None, None, None]
    assert check_winner(board) is None


def test_draw_state_no_winner():
    board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    assert check_winner(board) is None	

def test_make_move_on_taken_cell_raises_error():
    board = empty_board()
    board = place_mark(board, 0, "X")
    with pytest.raises(ValueError):
        place_mark(board, 0, "X")


def test_cannot_move_after_game_won():
    board = ["X", "X", "X", None, None, None, None, None, None]
    assert check_winner(board) == "X"

    with pytest.raises(ValueError):
        place_mark(board, 0, "X")