import pandas as pd
from pathlib import Path

from app.db.models import QB, Team
from app.db.session import engine

from sqlalchemy.orm import Session
from sqlalchemy import inspect, Engine

from app import db_path


def load_color_data(engine: Engine):
    inspector = inspect(engine)
    with Session(engine) as session:

        if "teams" in inspector.get_table_names():
            if not session.query(Team).first():
                df = pd.read_csv(db_path / 'data' / 'team_colors.csv')

                for _, row in df.iterrows():
                    item = Team(abbr=row.team_abbr, 
                                primary_color=row.team_color,
                                secondary_color=row.team_color2)
                    session.add(item)
        session.commit()


def load_player_data(engine: Engine):
    inspector = inspect(engine)
    with Session(engine) as session:
        if "quarterbacks" in inspector.get_table_names():
            if not session.query(QB).first():
                df = pd.read_csv(db_path / 'data' / 'qb_names.csv')

                for _, row in df.iterrows():
                    item = QB(id=row.player_id,
                            name=row.player_name,
                            team_abbr=row.team)
                    session.add(item)
        session.commit()
