from app.logic import empty_board, place_mark, check_winner, is_draw


def test_win_row():
    # Arrange
    board = empty_board()

    # Act
    board = place_mark(board, 0, "X")
    board = place_mark(board, 1, "X")
    board = place_mark(board, 2, "X")

    # Assert
    assert check_winner(board) == "X"


def test_draw():
    # A full board with no winner
    board = [
        "X", "O", "X",
        "X", "O", "O",
        "O", "X", "X",
    ]

    assert is_draw(board)
