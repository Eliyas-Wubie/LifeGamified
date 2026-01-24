from sqlalchemy import String, Integer, JSON, ForeignKey, DATETIME, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.db.base import Base
from typing import Any


# Main Tables
class BaseActivityORM(Base):
    __tablename__="base_activities"
    
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    baseXP: Mapped[int] = mapped_column(Integer, nullable=False)
    strain: Mapped[list["BaseActivityAttributesORM"]] = relationship(
        back_populates="base_activity",
        cascade="all, delete-orphan"
    )

class CompoundActivityORM(Base):
    __tablename__ = "compound_activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    xp: Mapped[int] = mapped_column(nullable=False)
    base_activities_gage: Mapped[list["CompoundActivityBaseActivityORM"]] = relationship(
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
    bonus:Mapped[dict[str,Any]]=mapped_column(JSON, nullable=True)
    
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
    
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    name:Mapped[str]=mapped_column(String, nullable=False)
    difficulty:Mapped[int]=mapped_column(Integer, nullable=False)
    
    title_links:Mapped[list["AccomplishmentsTitlesORM"]]=relationship(
        back_populates="accomplishments",
        cascade="all, delete-orphan"
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
    accomplishment_link:Mapped[list["AccomplishmentsTitlesORM"]]=relationship(
        back_populates="titles",
        cascade="all, delete-orphan"
    )
    
class AttributesORM(Base):
    __tablename__ = "attributes"
    
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False)
    area:Mapped[str]=mapped_column(String, nullable=False)
    custom:Mapped[bool]=mapped_column(Boolean, nullable=False)
    current_value:Mapped[int]=mapped_column(Boolean, nullable=False)
    contributor_activities:Mapped["BaseActivityAttributesORM"]=relationship(
        back_populates="attributes"
    )
    # no relation here


# ASSOCIATIONS

class BaseActivityAttributesORM(Base):
    __tablename__ = "base_activity_attributes"
    
    base_activity_id: Mapped[int] = mapped_column(
        ForeignKey("base_activities.id"), 
        primary_key=True
        )
    attributes_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.id"), 
        primary_key=True
        )
    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 10", name="rating_range"),
    )
    base_activity: Mapped["BaseActivityORM"]= relationship(
        back_populates="strain"
        )
    attributes: Mapped["AttributesORM"]= relationship(
        back_populates="contributor_activities"
        )
    
class CompoundActivityBaseActivityORM(Base):
    __tablename__ = "compound_activity_base_activity"
    
    compound_activity_id: Mapped[int] = mapped_column(
        ForeignKey("compound_activity.id"),
        primary_key=True
    )
    
    base_activity_id: Mapped[int] = mapped_column(
        ForeignKey("base_activities.id"), 
        primary_key=True
        )
    
    compound_activity: Mapped["CompoundActivityORM"] = relationship(
        back_populates="base_activities_gage"
    )

class CompoundActivityProfessionORM(Base): # 
    __tablename__ = "compound_activity_profession"

    compound_activity_id: Mapped[int] = mapped_column(
        ForeignKey("compound_activity.id"),
        primary_key=True
    )

    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id"),
        primary_key=True
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 10", name="rating_range"),
    )

    # relationships
    compound_activity: Mapped["CompoundActivityORM"] = relationship(
        back_populates="profession_links"
    )
    profession: Mapped["ProfessionORM"] = relationship(
        back_populates="compound_activity_links"
    )

class MissionCompoundActivityORM(Base):
    __tablename__ = "mission_compound_activity"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    compound_activity_id:Mapped[int]=mapped_column(
        ForeignKey("compound_activity.id"),
        primary_key=True
    )
    mission:Mapped["MissionsORM"]=relationship(
        back_populates="compound_activities"
    )
    
class MissionAccomplishmentORM(Base):
    __tablename__ = "mission_accomplishments"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    accomplishments_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
    )
    mission:Mapped["MissionsORM"]=relationship(
        back_populates="accomplishments"
    )

class MissionProfessionORM(Base):
    __tablename__ = "mission_profession"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    profession_id:Mapped[int]=mapped_column(
        ForeignKey("professions.id"),
        primary_key=True
    )
    rating:Mapped[int]=mapped_column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 10", name="rating_range"),
    )
    mission:Mapped["MissionsORM"]=relationship(
        back_populates="profession"
    )
    profession:Mapped["ProfessionORM"]=relationship(
        back_populates="mission_links"
    )

class AccomplishmentsTitlesORM(Base):
    __tablename__ = "accomplishments_title"
    
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
        )
    title_id:Mapped[int]=mapped_column(
        ForeignKey("titles.id"),
        primary_key=True
        )
    accomplishments:Mapped["AccomplishmentORM"]=relationship(
        back_populates="title_links"
        )
    titles:Mapped["TitlesORM"]=relationship(
        back_populates="accomplishment_link"
        )
    
class AccomplishmentsAttributesORM(Base):
    __tablename__="accomplishments_attributes"
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
        )
    attribute_id:Mapped[int]=mapped_column(
        ForeignKey("attributes.id"),
        primary_key=True
        )
    accomplishments:Mapped["AccomplishmentORM"]=relationship(
        back_populates="attribute_link"
        )

class AccomplishmentsProfessionORM(Base):
    __tablename__ = "accomplishments_professions"
    
    accomplishment_id:Mapped[int]=mapped_column(
        ForeignKey("accomplishments.id"),
        primary_key=True
        )
    proffession_id:Mapped[int]=mapped_column(
        ForeignKey("professions.id"),
        primary_key=True
        )
    accomplishments:Mapped["AccomplishmentORM"]=relationship(
        back_populates="profession_link"
        )
    professions_link:Mapped["ProfessionORM"]=relationship(
        back_populates="accomplishments_link"
        )



