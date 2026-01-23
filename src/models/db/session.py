from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database (file-based)
engine = create_engine("sqlite:///local_life_gamified.db", echo=True)

# Factory to create sessions
SessionLocal = sessionmaker(bind=engine)
