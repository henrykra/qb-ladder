from app.db.session import engine
from sqlalchemy import text
import pandas as pd

def get_colors(id: int) -> tuple[str, str]:
    """Get a player's team's primary and secondary color by player id"""
    with engine.connect() as connection:

        command = """SELECT t.primary_color, t.secondary_color
FROM teams t, quarterbacks q
WHERE q.id = :id AND q.team_abbr = t.abbr;"""

        result = connection.execute(text(command), {'id': id})

        row = result.first()

        return row


def get_player(id: int) -> str:
    """Get a player's name, first name, and last name by player id."""
    with engine.connect() as connection:

        command = """SELECT q.name, q.first_name, q.last_name FROM quarterbacks q
WHERE q.id = :id;"""
        result = connection.execute(text(command), {'id': id})

        row = result.first()

        return row
    

def get_player_stats(id: int) -> str:
    """Get a player's 2024 stats by player id."""
    with engine.connect() as connection:
        command = """SELECT * FROM stats s,
WHERE s.player_id = :id;"""
        result = connection.execute(text(command), {'id': id})

        row = result.first()
        return row


def get_qb_data() -> pd.DataFrame:
    """Get all quarterbacks' 2024 stats."""
    return pd.read_sql_table('stats', engine)