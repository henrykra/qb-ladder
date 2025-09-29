from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB stored locally in app/db/test.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/quarterbacks.db"

# For SQLite, need check_same_thread=False when using with multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()