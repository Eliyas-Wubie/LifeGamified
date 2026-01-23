from sqlalchemy import String, Integer, JSON, ForeignKey, CheckConstraint, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from typing import Any

# Main Tables
class BaseActivityORM(Base):
    __tablename__="base_activities"
    
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    baseXP: Mapped[int] = mapped_column(Integer, nullable=False)
    strain: Mapped[list["BaseActivityAttributesORM"]] = relationship(
        back_populates="base_activity"
    )

class CompoundActivityORM(Base):
    __tablename__ = "compound_activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    xp: Mapped[int] = mapped_column(nullable=False)
    base_activities_gage: Mapped[list["CompoundActivityProfessionORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )
    profession_links: Mapped[list["CompoundActivityProfessionORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )

class MissionsORM(Base):
    __tablename__ = "missions"
    id:Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False)
    deadline: Mapped[DATETIME]=mapped_column(DATETIME, nullable=True)
    bonus:Mapped[dict[str:Any]]=mapped_column(JSON, nullable=True)
    
    compound_activities:Mapped["MissionCompoundActivityORM"]=relationship(
        back_populates="mission"
    )
    
    accomplishments:Mapped["MissionAccomplishmentORM"]=relationship(
        back_populates="mission"
    )
    
    profession:Mapped["MissionProfessionORM"]=relationship(
        back_populates="mission"
    )
        
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
    
    compound_activity_links: Mapped[list["CompoundActivityProfessionORM"]] = relationship(
        back_populates="profession",
        cascade="all, delete-orphan"
    )
    mission_links: Mapped[list["MissionProfessionORM"]] = relationship(
        back_populates="profession",
        cascade="all, delete-orphan"
    )
    accomplishments_link:Mapped["AccomplishmentsProfessionORM"]=relationship(
        back_populates="professions_link"
    )
    # relation to accomplishments


class AccomplishmentORM(Base):
    __tablename__="accomplishments"
    
    id:Mapped[int]=mapped_column(Integer, nullable=False)
    name:Mapped[str]=mapped_column(String, nullable=False)
    difficulty:Mapped[int]=mapped_column(Integer, nullable=False)
    
    title_links:Mapped["AccomplishmentsTitlesORM"]=relationship(
        back_populates="accomplishments"
        )
    attribute_link:Mapped["AccomplishmentsAttributesORM"]=relationship(
        back_populates="accomplishments"
    )
    profession_link:Mapped["AccomplishmentsProfessionORM"]=relationship(
        back_populates="accomplishments"
    )

class TitlesORM(Base):
    __tablename__ =  "titles"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(Integer, nullable=False)
    description: Mapped[str]=mapped_column(String, nullable=False)
    # relation to accomplishments
    accomplishment_link:Mapped["AccomplishmentsTitlesORM"]=relationship(
        back_populates="accomplishments"
    )
    
class AttributesORM(Base):
    __tablename__ = "attributes"
    
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False)
    domain:Mapped[str]=mapped_column(str, nullable=False)
    custom:Mapped[bool]=mapped_column(bool, nullable=False)
    current_value:Mapped[int]=mapped_column(bool, nullable=False)
    contributor_activities:Mapped("BaseActivityAttributesORM")=relationship(
        back_populates="attributes"
    )
    # no relation here
