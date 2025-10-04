from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.llm_client import TestClient, GeminiClient
from app.api.schema import ChatQuery, ChatResponse, ColorResponse, PlayerResponse
from app.db.queries import get_colors, get_player, get_qb_data
from app.services.prompt_utils import load_no_data_template, load_data_template
from pydantic import BaseModel

from app.db.queries import *


class SampleQuery(BaseModel):
    prompt: str

router = APIRouter()

@router.get('/argue/', response_model=ChatResponse)
async def argue():
    client = TestClient()

    return ChatResponse(response=client.chat())


@router.post('/stream/')
async def stream(query: ChatQuery):
    # initialize LLM client
    client = GeminiClient()

    # ? Query DB for player names from ids
    names = [get_player(qb_id)[0] for qb_id in query.qb_list]
    data = get_qb_data()

    # colllect prompt template
    if True:
        prompt = load_data_template(query.qb_list, names, data)
    else:
        prompt = load_no_data_template(names)

    # Insert supporting statistics into prompt template

    # Call to llm client
    gen = client.chat_streaming(prompt=prompt)

    return StreamingResponse(gen, media_type="text/event-stream")


@router.get('/color/{id}')
async def query(id: int) -> ColorResponse:
    c1, c2 = get_colors(id)

    return ColorResponse(primary_color=c1, secondary_color=c2)

@router.get('/player/{id}')
async def query(id: int) -> PlayerResponse:

    name, first_name, last_name = get_player(id)
    return PlayerResponse(name=name, first_name=first_name, last_name=last_name, id=id)