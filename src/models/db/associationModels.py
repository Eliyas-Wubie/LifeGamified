from sqlalchemy import String, Integer, JSON, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from typing import Any



# Association Tables
class BaseActivityAttributesORM(Base):
    __tablename__ = "base_activity_attributes"
    
    base_activity_id: Mapped[int] = mapped_column(
        ForeignKey("base_activity.id"), 
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
        ForeignKey("base_activity.id"), 
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
        ForeignKey("compound_activity.id")
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
        ForeignKey("accomplishments.id")
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
        ForeignKey("profession.id")
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
        ForeignKey("accomplishment.id"),
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
        ForeignKey("accomplishment.id"),
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
        ForeignKey("accomplishment.id"),
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
        back_populates="accomplishment_link"
        )






