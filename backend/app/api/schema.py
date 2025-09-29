from pydantic import BaseModel



class ChatQuery(BaseModel):
    qb_list: list[int, int, int, int]

class ChatResponse(BaseModel):
    response: str

class ColorQuery(BaseModel):
    player_id: int


class ColorResponse(BaseModel):
    primary_color: str
    secondary_color: str


class PlayerResponse(BaseModel):
    name: str
    id: int
