from pydantic import BaseModel


class ChatQuery(BaseModel):
    """Query model for LLM argument. Takes user's ranking."""
    qb_list: list[int, int, int, int]


class ChatResponse(BaseModel):
    """Response for non-streaming LLM call."""
    response: str


class ColorQuery(BaseModel):
    """Query model for getting team colors by player id."""
    player_id: int


class ColorResponse(BaseModel):
    """Response model for team colors."""
    primary_color: str
    secondary_color: str


class PlayerResponse(BaseModel):
    """Response model for player name info."""
    first_name: str
    last_name: str
    name: str
    id: int
