from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.db.base import Base
from src.models.db import models # type: ignore


# 1️⃣ Create the engine (file-based SQLite)
engine = create_engine("sqlite:///local_life_gamified.db", echo=True)

# 2️⃣ Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# 3️⃣ Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
