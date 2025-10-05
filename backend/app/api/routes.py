from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.llm_client import TestClient, GeminiClient
from app.api.schema import ChatQuery, ChatResponse, ColorResponse, PlayerResponse
from app.db.queries import get_colors, get_player, get_qb_data
from app.services.prompt_utils import load_no_data_template, load_data_template

from app.db.queries import *


router = APIRouter()

@router.post('/stream/')
async def stream(query: ChatQuery):
    """Endpoint for LLM streaming
    
    Arguments
    ---------
    query : ChatQuery
        Query to LLM containing the user's ranking
        
    Returns
    -------
        Streaming response via the generator returned by the llm call. 
    """
    # initialize LLM client
    client = GeminiClient()

    # Query DB for player names from ids
    names = [get_player(qb_id)[0] for qb_id in query.qb_list]

    # Get all QB data
    data = get_qb_data()

    # colllect prompt template & load data
    if True:
        prompt = load_data_template(query.qb_list, names, data)
    else:
        prompt = load_no_data_template(names)

    # Call to llm client
    gen = client.chat_streaming(prompt=prompt)

    return StreamingResponse(gen, media_type="text/event-stream")


@router.get('/color/{id}')
async def query(id: int) -> ColorResponse:
    """Gets team colors for a given player's id."""
    c1, c2 = get_colors(id)

    return ColorResponse(primary_color=c1, secondary_color=c2)

@router.get('/player/{id}')
async def query(id: int) -> PlayerResponse:
    """Gets player name for a given player's id."""
    name, first_name, last_name = get_player(id)
    return PlayerResponse(name=name, first_name=first_name, last_name=last_name, id=id)