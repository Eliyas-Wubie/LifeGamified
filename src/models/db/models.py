from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base

class ProfessionORM(Base):
    __tablename__ = "professions"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("professions.id"))

    sub_professions: Mapped[list["ProfessionORM"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    parent: Mapped["ProfessionORM | None"] = relationship(
        back_populates="sub_professions",
        remote_side=[id]
    )
