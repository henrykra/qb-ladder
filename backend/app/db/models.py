from sqlalchemy.orm import  relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.session import Base


# Create models
class QB(Base):
    """Model representing rows in the basic QB info table."""
    __tablename__ = 'quarterbacks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    team_abbr = Column(Integer, ForeignKey("teams.abbr"))
    
    # relationships
    team = relationship("Team", back_populates="quarterbacks")

    def __repr__(self) -> str:
        return f"QB(name={self.name!r}, id={self.id!r}, team_abbr={self.team_abbr!r})"


class Team(Base):
    """Model representing rows in the team color info table."""
    __tablename__ = 'teams'

    abbr = Column(String, primary_key=True, index=True)
    primary_color = Column(String)
    secondary_color = Column(String)

    # relationships
    quarterbacks = relationship("QB", back_populates="team") # one-to-many

    def __repr__(self) -> str:
        return f"Team(abbr={self.abbr!r})"
