from datetime import datetime, date, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Date, Boolean, ForeignKey

from app.auth.auth_models import User

class Faculty(User):
    __tablename__='faculty'

    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    is_verified: sqlo.Mapped[bool] = sqlo.mapped_column(default=False)
    
    positions: sqlo.WriteOnlyMapped[ResearchPosition] = relationship(back_populates='faculty')
    __mapper_args__ = {
    'polymorphic_identity': 'Faculty'
    }
    

class ResearchPosition(db.Model):
    __tablename__ = "research_position"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Required fields from assignment
    title:               Mapped[str] = mapped_column(String(150), nullable=False)
    description:         Mapped[str] = mapped_column(Text, nullable=False)
    start_date:          Mapped[date] = mapped_column(Date, nullable=False)
    end_date:            Mapped[date] = mapped_column(Date, nullable=False)
    team_size:           Mapped[int] = mapped_column(Integer, nullable=False)
    min_gpa:             Mapped[float] = mapped_column(nullable=False)
    reference_required:  Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps (optional but useful)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # Foreign key → Faculty who created the position
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    faculty: Mapped[Faculty] = relationship(back_populates="positions")

    # Many-to-many relationships
    preferred_majors: Mapped[list["Major"]] = relationship(
        secondary="position_majors"
    )
    research_topics: Mapped[list["ResearchTopic"]] = relationship(
        secondary="position_topics"
    )
    programming_languages: Mapped[list["ProgrammingLanguage"]] = relationship(
        secondary="position_languages"
    )
    required_courses: Mapped[list["Course"]] = relationship(
        secondary="position_courses"
    )

    # Applications (one-to-many)
    applications: Mapped[list["Application"]] = relationship(
        back_populates="position"
    )

    def get_faculty_name(self):
        first = db.session.scalars(self.faculty.get_firstname())
        last = db.session.scalars(self.faculty.get_lastname())
        return first + ' ' + last

    
class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class ResearchTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class ProgrammingLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  
    name = db.Column(db.String(150), nullable=False)



# --- Association Table: ResearchPosition - Majors ---
position_majors = db.Table(
    "position_majors",
    db.Column("position_id", db.Integer, db.ForeignKey("research_position.id"), primary_key=True),
    db.Column("major_id", db.Integer, db.ForeignKey("major.id"), primary_key=True)
)

# --- Association Table: ResearchPosition - Research Topics ---
position_topics = db.Table(
    "position_topics",
    db.Column("position_id", db.Integer, db.ForeignKey("research_position.id"), primary_key=True),
    db.Column("topic_id", db.Integer, db.ForeignKey("research_topic.id"), primary_key=True)
)

# --- Association Table: ResearchPosition - Programming Languages ---
position_languages = db.Table(
    "position_languages",
    db.Column("position_id", db.Integer, db.ForeignKey("research_position.id"), primary_key=True),
    db.Column("language_id", db.Integer, db.ForeignKey("programming_language.id"), primary_key=True)
)

# --- Association Table: ResearchPosition - Required Courses ---
position_courses = db.Table(
    "position_courses",
    db.Column("position_id", db.Integer, db.ForeignKey("research_position.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True)
)