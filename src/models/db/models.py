from sqlalchemy import String, Integer, JSON, ForeignKey, DATETIME, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.db.base import Base
from typing import Any


# Main Tables
class BaseActivityORM(Base):
    __tablename__="base_activities"
    
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_type: Mapped[str]=mapped_column(String, nullable=False)
    attributes: Mapped[list["BaseActivityAttributeORM"]] = relationship(
        back_populates="base_activity",
        cascade="all, delete-orphan"
    )
    compound_activities: Mapped[list["CompoundActivityBaseActivityORM"]] = relationship(
        back_populates="base_activity",
        cascade="all, delete-orphan"
    )

class CompoundActivityORM(Base):
    __tablename__ = "compound_activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    xp: Mapped[int] = mapped_column(nullable=False)
    base_activities: Mapped[list["CompoundActivityBaseActivityORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )
    professions: Mapped[list["CompoundActivityProfessionORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )
    missions: Mapped[list["MissionCompoundActivityORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )

class MissionORM(Base):
    __tablename__ = "missions"
    id:Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False)
    deadline: Mapped[DATETIME]=mapped_column(DATETIME, nullable=True)
    bonus:Mapped[dict[str,Any]]=mapped_column(JSON, nullable=True)
    
    compound_activities:Mapped[list["MissionCompoundActivityORM"]]=relationship(
        back_populates="mission"
    )
    
    accomplishments:Mapped[list["MissionAccomplishmentORM"]]=relationship(
        back_populates="mission"
    )
    
    professions:Mapped[list["MissionProfessionORM"]]=relationship(
        back_populates="mission"
    )
          
class ProfessionORM(Base):
    __tablename__ = "professions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
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
    
    compound_activities: Mapped[list["CompoundActivityProfessionORM"]] = relationship(
        back_populates="profession",
        cascade="all, delete-orphan"
    )
    missions: Mapped[list["MissionProfessionORM"]] = relationship(
        back_populates="profession",
        cascade="all, delete-orphan"
    )
    accomplishments:Mapped["AccomplishmentProfessionORM"]=relationship(
        back_populates="profession"
    )
    # relation to accomplishments

class AccomplishmentORM(Base):
    __tablename__="accomplishments"
    
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    name:Mapped[str]=mapped_column(String, nullable=False)
    difficulty:Mapped[int]=mapped_column(Integer, nullable=False)
    
    titles:Mapped[list["AccomplishmentTitleORM"]]=relationship(
        back_populates="accomplishment",
        cascade="all, delete-orphan"
        )
    attributes:Mapped[list["AccomplishmentAttributeORM"]]=relationship(
        back_populates="accomplishment"
    )
    professions:Mapped[list["AccomplishmentProfessionORM"]]=relationship(
        back_populates="accomplishment"
    )
    missions:Mapped[list["MissionAccomplishmentORM"]]=relationship(
        back_populates="accomplishment"
    )

class TitleORM(Base):
    __tablename__ =  "titles"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(Integer, nullable=False, unique=True)
    description: Mapped[str]=mapped_column(String, nullable=False)
    accomplishments:Mapped[list["AccomplishmentTitleORM"]]=relationship(
        back_populates="title",
        cascade="all, delete-orphan"
    )
    
class AttributeORM(Base):
    __tablename__ = "attributes"
    
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False, unique=True)
    area:Mapped[str]=mapped_column(String, nullable=False)
    custom:Mapped[bool]=mapped_column(Boolean, nullable=False)
    current_value:Mapped[int]=mapped_column(Boolean, nullable=False)
    base_activities:Mapped[list["BaseActivityAttributeORM"]]=relationship(
        back_populates="attribute"
    )
    accomplishments:Mapped[list["AccomplishmentAttributeORM"]]=relationship(
        back_populates="attribute"
    )


# ASSOCIATIONS

class BaseActivityAttributeORM(Base):
    __tablename__ = "base_activities_attributes"
    
    base_activity_id: Mapped[int] = mapped_column(
        ForeignKey("base_activities.id"), 
        primary_key=True
        )
    attributes_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.id"), 
        primary_key=True
        )
    load: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )
    base_activity: Mapped["BaseActivityORM"]= relationship(
        back_populates="attributes"
        )
    attribute: Mapped["AttributeORM"]= relationship(
        back_populates="base_activities"
        )
    
class CompoundActivityBaseActivityORM(Base):
    __tablename__ = "compound_activities_base_activities"
    
    compound_activity_id: Mapped[int] = mapped_column(
        ForeignKey("compound_activities.id"),
        primary_key=True
    )
    
    base_activity_id: Mapped[int] = mapped_column(
        ForeignKey("base_activities.id"), 
        primary_key=True
        )
    load: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )
    base_activity: Mapped["BaseActivityORM"] = relationship(
        back_populates="compound_activities"
    )
    compound_activity: Mapped["CompoundActivityORM"] = relationship(
        back_populates="base_activities"
    )

class CompoundActivityProfessionORM(Base): # 
    __tablename__ = "compound_activities_profession"

    compound_activity_id: Mapped[int] = mapped_column(
        ForeignKey("compound_activities.id"),
        primary_key=True
    )

    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id"),
        primary_key=True
    )

    load: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )

    compound_activity: Mapped["CompoundActivityORM"] = relationship(
        back_populates="professions"
    )
    profession: Mapped["ProfessionORM"] = relationship(
        back_populates="compound_activities"
    )

class MissionCompoundActivityORM(Base):
    __tablename__ = "mission_compound_activities"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    compound_activity_id:Mapped[int]=mapped_column(
        ForeignKey("compound_activities.id"),
        primary_key=True
    )
    load: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )

    mission:Mapped["MissionORM"]=relationship(
        back_populates="compound_activities"
    )
    compound_activity:Mapped["CompoundActivityORM"]=relationship(
        back_populates="missions"
    )
    
class MissionAccomplishmentORM(Base):
    __tablename__ = "missions_accomplishments"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
    )
    mission:Mapped["MissionORM"]=relationship(
        back_populates="accomplishments"
    )
    accomplishment:Mapped["AccomplishmentORM"]=relationship(
        back_populates="missions"
    )

class MissionProfessionORM(Base):
    __tablename__ = "missions_professions"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    profession_id:Mapped[int]=mapped_column(
        ForeignKey("professions.id"),
        primary_key=True
    )
    load:Mapped[int]=mapped_column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )
    mission:Mapped["MissionORM"]=relationship(
        back_populates="professions"
    )
    profession:Mapped["ProfessionORM"]=relationship(
        back_populates="missions"
    )

class AccomplishmentTitleORM(Base):
    __tablename__ = "accomplishments_titles"
    
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
        )
    title_id:Mapped[int]=mapped_column(
        ForeignKey("titles.id"),
        primary_key=True
        )
    accomplishment:Mapped["AccomplishmentORM"]=relationship(
        back_populates="titles"
        )
    title:Mapped["TitleORM"]=relationship(
        back_populates="accomplishments"
        )
    
class AccomplishmentAttributeORM(Base):
    __tablename__="accomplishments_attributes"
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
        )
    attribute_id:Mapped[int]=mapped_column(
        ForeignKey("attributes.id"),
        primary_key=True
        )
    load:Mapped[int]=mapped_column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )
    accomplishment:Mapped["AccomplishmentORM"]=relationship(
        back_populates="attributes"
        )
    attribute:Mapped["AttributeORM"]=relationship(
        back_populates="accomplishments"
        )

class AccomplishmentProfessionORM(Base):
    __tablename__ = "accomplishments_professions"
    
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
        )
    profession_id:Mapped[int]=mapped_column(
        ForeignKey("professions.id"),
        primary_key=True
        )
    load:Mapped[int]=mapped_column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint("load BETWEEN 1 AND 10", name="load_range"),
    )
    accomplishment:Mapped["AccomplishmentORM"]=relationship(
        back_populates="professions"
        )
    profession:Mapped["ProfessionORM"]=relationship(
        back_populates="accomplishments"
        )
