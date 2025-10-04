# fastapi entrypoint

from fastapi import FastAPI
from app.api.routes import router as api_router

from sqlalchemy import inspect
from app.db.session import Base, engine
from app.db.models import QB, Team
from app.db.import_data import load_color_data, load_player_info, load_player_stats

# startup database
Base.metadata.create_all(engine)

# seed data
load_player_info(engine)
load_color_data(engine)
load_player_stats(engine)

app = FastAPI()

@app.get('/')
def root():
    return {"response": "api running.",
            "tables": inspect(engine).get_table_names()}


app.include_router(api_router, prefix='/api')
