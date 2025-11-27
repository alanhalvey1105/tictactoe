from pydantic import BaseModel, Field
from typing import Optional, List

class GameCreate(BaseModel):
    """Request model for creating a new game."""
    player_name: str = Field(..., description="Name of the human player")


class MoveRequest(BaseModel):
    """Request model for making a move in the game."""
    player_name: str = Field(..., description="Name of the player making the move")
    position: int = Field(..., ge=0, le=8, description="Board index (0–8)")


class GameResponse(BaseModel):
    """Response model representing a full game state."""
    id: str
    board: List[Optional[str]] = Field(..., description="Board cells: 'X', 'O', or None")
    player: Optional[str] = Field(None, description="Player assigned to this game")
    winner: Optional[str] = Field(None, description="Winner ('X', 'O', or None)")
    is_draw: bool = Field(..., description="True if the game ended in a draw")

