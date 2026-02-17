from sqlalchemy import String, Integer, JSON, ForeignKey, DateTime, Boolean, CheckConstraint, Float
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.db.base import Base
from typing import Any
from datetime import datetime
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )



# Main Tables

class BaseActivityORM(TimestampMixin,Base):
    __tablename__="base_activities"
    
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    xp: Mapped[float] = mapped_column(Float, nullable=False)
    activity_type: Mapped[str]=mapped_column(String, nullable=False)
    attributes: Mapped[list["BaseActivityAttributeORM"]] = relationship(
        back_populates="base_activity",
        cascade="all, delete-orphan"
    )
    compound_activities: Mapped[list["BaseActivityCompoundActivityORM"]] = relationship(
        back_populates="base_activity",
        cascade="all, delete-orphan"
    )

class CompoundActivityORM(TimestampMixin,Base):
    __tablename__ = "compound_activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    xp: Mapped[float] = mapped_column(Float, nullable=False)
    tags: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSON),default=list,)
    base_activities: Mapped[list["BaseActivityCompoundActivityORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )
    professions: Mapped[list["CompoundActivityProfessionORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )
    missions: Mapped[list["CompoundActivityMissionORM"]] = relationship(
        back_populates="compound_activity",
        cascade="all, delete-orphan"
    )

class MissionORM(TimestampMixin,Base):
    __tablename__ = "missions"
    id:Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False)
    description: Mapped[str]=mapped_column(String, nullable=True)
    deadline: Mapped[datetime]=mapped_column(DateTime, nullable=True)
    bonus:Mapped[list[dict[str,Any]]]=mapped_column(MutableList.as_mutable(JSON), nullable=True)
    
    compound_activities:Mapped[list["CompoundActivityMissionORM"]]=relationship(
        back_populates="mission"
    )
    
    accomplishments:Mapped[list["MissionAccomplishmentORM"]]=relationship(
        back_populates="mission"
    )
    
    professions:Mapped[list["MissionProfessionORM"]]=relationship(
        back_populates="mission"
    )
          
class ProfessionORM(TimestampMixin,Base):
    __tablename__ = "professions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    points: Mapped[float] = mapped_column(Float, nullable=False)
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
    
    accomplishments:Mapped[list["AccomplishmentProfessionORM"]]=relationship(
        back_populates="profession"
    )
    # relation to accomplishments

class AccomplishmentORM(TimestampMixin,Base):
    __tablename__="accomplishments"
    
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    name:Mapped[str]=mapped_column(String, nullable=False)
    difficulty:Mapped[int]=mapped_column(Integer, nullable=False)
    description:Mapped[str] = mapped_column(String, nullable=False)
    status:Mapped[str] = mapped_column(String, nullable=False, default="locked")
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

class TitleORM(TimestampMixin,Base):
    __tablename__ =  "titles"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(Integer, nullable=False, unique=True)
    description: Mapped[str]=mapped_column(String, nullable=True)
    status:Mapped[str] = mapped_column(String, nullable=False, default="locked")
    accomplishments:Mapped[list["AccomplishmentTitleORM"]]=relationship(
        back_populates="title",
        cascade="all, delete-orphan"
    )
    
class AttributeORM(TimestampMixin,Base):
    __tablename__ = "attributes"
    
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String, nullable=False, unique=True)
    area:Mapped[str]=mapped_column(String, nullable=False)
    custom:Mapped[bool]=mapped_column(Boolean, nullable=False)
    current_value:Mapped[float]=mapped_column(Float, nullable=False)
    base_activities:Mapped[list["BaseActivityAttributeORM"]]=relationship(
        back_populates="attribute"
    )
    accomplishments:Mapped[list["AccomplishmentAttributeORM"]]=relationship(
        back_populates="attribute"
    )

class DailyReportORM(TimestampMixin,Base):
    __tablename__ = "daily_reports"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    date:Mapped[datetime]=mapped_column(DateTime, nullable=False)
    compound_activities:Mapped[list["DailyReportCompoundActivityORM"]]=relationship(back_populates="daily_report")
    missions:Mapped[list["DailyReportMissionORM"]]=relationship(back_populates="daily_report")

class StatusORM(TimestampMixin,Base):
    __tablename__ = "status"
    _instance = None
    
    def __new__(cls, *args: Any, **kwargs:Any): # but this dose not work on persistent instance i.e only one row
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance        
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String,  nullable= False)
    xp:Mapped[float] =  mapped_column(Float, nullable=False)
    level:Mapped[int] = mapped_column(Integer, nullable=False)
    attributes:Mapped[list["StatusAttributeORM"]]=relationship(back_populates="status")
    titles:Mapped[list["StatusTitleORM"]]=relationship(back_populates="status")
  

# ASSOCIATIONS

class BaseActivityAttributeORM(TimestampMixin,Base):
    __tablename__ = "base_activities_attributes"
    
    base_activity_id: Mapped[int] = mapped_column(
        ForeignKey("base_activities.id"), 
        primary_key=True
        )
    attribute_id: Mapped[int] = mapped_column(
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
    
class BaseActivityCompoundActivityORM(TimestampMixin,Base):
    __tablename__ = "base_activities_compound_activities"
    
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

class CompoundActivityMissionORM(TimestampMixin,Base): # 
    __tablename__ = "compound_activities_missions"
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
    )
    compound_activity_id:Mapped[int]=mapped_column(
        ForeignKey("compound_activities.id"),
        primary_key=True
    )
    mission:Mapped["MissionORM"]=relationship(
        back_populates="compound_activities"
    )
    compound_activity:Mapped["CompoundActivityORM"]=relationship(
        back_populates="missions"
    )

class CompoundActivityProfessionORM(TimestampMixin,Base): # 
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

class MissionAccomplishmentORM(TimestampMixin,Base):
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

class MissionProfessionORM(TimestampMixin,Base):
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

class AccomplishmentAttributeORM(TimestampMixin,Base):
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

class AccomplishmentTitleORM(TimestampMixin,Base):
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
    
class AccomplishmentProfessionORM(TimestampMixin,Base):
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

class DailyReportCompoundActivityORM(TimestampMixin,Base):
    __tablename__ = "daily_reports_compound_activities"
    
    daily_report_id:Mapped[int]=mapped_column(
        ForeignKey("daily_reports.id"),
        primary_key=True
        )
    compound_activity_id:Mapped[int]=mapped_column(
        ForeignKey("compound_activities.id"),
        primary_key=True
        )
    daily_report:Mapped["DailyReportORM"]=relationship(
        back_populates="compound_activities"
        )
    compound_activity:Mapped["CompoundActivityORM"]=relationship()
    
class DailyReportMissionORM(TimestampMixin,Base):
    __tablename__ = "daily_reports_missions"
    
    daily_report_id:Mapped[int]=mapped_column(
        ForeignKey("daily_reports.id"),
        primary_key=True
        )
    mission_id:Mapped[int]=mapped_column(
        ForeignKey("missions.id"),
        primary_key=True
        )
    daily_report:Mapped["DailyReportORM"]=relationship(
        back_populates="missions"
        )
    mission:Mapped["MissionORM"]=relationship()

class StatusAttributeORM(TimestampMixin,Base):
    __tablename__ = "status_attributes"
    
    status_id:Mapped[int]=mapped_column(
        ForeignKey("status.id"),
        primary_key=True
        )
    attribute_id:Mapped[int]=mapped_column(
        ForeignKey("attributes.id"),
        primary_key=True
        )
    status:Mapped["StatusORM"]=relationship(
        back_populates="attributes"
        )
    attribute:Mapped["AttributeORM"]=relationship()
    
class StatusTitleORM(TimestampMixin,Base):
    __tablename__ = "status_titles"
    
    status_id:Mapped[int]=mapped_column(
        ForeignKey("status.id"),
        primary_key=True
        )
    title_id:Mapped[int]=mapped_column(
        ForeignKey("titles.id"),
        primary_key=True
        )
    status:Mapped["StatusORM"]=relationship(
        back_populates="titles"
        )
    title:Mapped["TitleORM"]=relationship()