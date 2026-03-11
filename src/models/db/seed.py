import json
from pathlib import Path

from sqlalchemy.orm import Session

from src.models.db.models import AttributeORM, BaseActivityORM, CompoundActivityORM


SEED_DIR = Path(__file__).resolve().parent / "seeds"


def _load_json(filename: str) -> list[dict]:
    with (SEED_DIR / filename).open("r", encoding="utf-8") as seed_file:
        return json.load(seed_file)


def _seed_attributes(session: Session) -> None:
    if session.query(AttributeORM).first():
        return

    rows = _load_json("attributes_seed.json")
    session.add_all(AttributeORM(**row) for row in rows)


def _seed_base_activities(session: Session) -> None:
    if session.query(BaseActivityORM).first():
        return

    rows = _load_json("base_activities_seed.json")
    session.add_all(BaseActivityORM(**row) for row in rows)


def _seed_compound_activities(session: Session) -> None:
    if session.query(CompoundActivityORM).first():
        return

    rows = _load_json("compound_activities_seed.json")
    session.add_all(CompoundActivityORM(**row) for row in rows)


def seed_database(session: Session) -> None:
    _seed_attributes(session)
    _seed_base_activities(session)
    _seed_compound_activities(session)
    session.commit()
