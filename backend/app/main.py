# fastapi entrypoint

from fastapi import FastAPI
from app.api.routes import router as api_router

from sqlalchemy import inspect
from app.db.session import Base, engine
from app.db.models import QB, Team
from app.db.import_data import load_color_data, load_player_data

# startup database
Base.metadata.create_all(engine)

# seed data
load_player_data(engine)
load_color_data(engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

@app.get('/')
def root():
    return {"response": "api running.",
            "tables": inspect(engine).get_table_names()}


app.include_router(api_router, prefix='/api')
