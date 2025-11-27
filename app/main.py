import uuid
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app.db import db, init_db
from app.logic import (
    empty_board, valid_move, place_mark,
    check_winner, is_draw, compute_computer_move
)
from contextlib import asynccontextmanager
from app.schema import GameCreate, MoveRequest, GameResponse


# ----------------------------------------------------------------------
# Lifecycle
# ----------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
async def get_game_or_404(game_id: str):
    """Fetch game or raise 404."""
    game = await db.fetch_one(
        "SELECT * FROM games WHERE id = :id",
        values={"id": game_id}
    )
    if not game:
        raise HTTPException(404, detail="Game not found")
    return game


def deserialize_board(row):
    """Row may return JSON/str depending on backend."""
    board = row["board"]
    return json.loads(board) if isinstance(board, str) else board


# ----------------------------------------------------------------------
# Create Game
# ----------------------------------------------------------------------
@app.post("/games", response_model=GameResponse)
async def create_game(req: GameCreate):
    game_id = str(uuid.uuid4())
    board = empty_board()

    await db.execute(
        """
        INSERT INTO games (id, board, player, winner)
        VALUES (:id, CAST(:board AS JSONB), :player, NULL)
        """,
        {
            "id": game_id,
            "board": json.dumps(board),
            "player": req.player_name,
        }
    )

    return GameResponse(
        id=game_id,
        board=board,
        player=req.player_name,
        winner=None,
        is_draw=False
    )


# ----------------------------------------------------------------------
# Join Game
# ----------------------------------------------------------------------
@app.post("/games/{game_id}/join", response_model=GameResponse)
async def join_game(game_id: str, req: GameCreate):
    game = await get_game_or_404(game_id)
    board = deserialize_board(game)
    return GameResponse(
        id=game["id"],
        board=board,
        player=game["player"],
        winner=game["winner"],
        is_draw=is_draw(board)
    )


# ----------------------------------------------------------------------
# Fetch Game
# ----------------------------------------------------------------------
@app.get("/games/{game_id}", response_model=GameResponse)
async def get_game(game_id: str):
    game = await get_game_or_404(game_id)
    board = deserialize_board(game)

    return GameResponse(
        id=game["id"],
        board=board,
        player=game["player"],
        winner=game["winner"],
        is_draw=is_draw(board)
    )


# ----------------------------------------------------------------------
# Make Move
# ----------------------------------------------------------------------
@app.post("/games/{game_id}/move", response_model=GameResponse)
async def make_move(game_id: str, req: MoveRequest):
    game = await get_game_or_404(game_id)
    board = deserialize_board(game)

    # Validate player move
    ok, reason = valid_move(board, req.position, "X")
    if not ok:
        raise HTTPException(400, detail=reason)

    # Apply player move
    board = place_mark(board, req.position, "X")
    winner = check_winner(board)

    # If game not over, make computer move
    if not winner:
        board = compute_computer_move(board)
        winner = check_winner(board)

    # Save updated board
    await db.execute(
        """
        UPDATE games
        SET board = CAST(:board AS JSONB),
            winner = :winner
        WHERE id = :id
        """,
        values={
            "board": json.dumps(board),
            "winner": winner,
            "id": game_id,
        }
    )

    return GameResponse(
        id=game_id,
        board=board,
        player=game["player"],
        winner=winner,
        is_draw=is_draw(board)
    )
