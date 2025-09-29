from app.db.session import engine
from sqlalchemy import text

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

    with engine.connect() as connection:

        command = """SELECT q.name FROM quarterbacks q
WHERE q.id = :id;"""
        result = connection.execute(text(command), {'id': id})

        row = result.first()

        return row[0]
