from datetime import datetime, date, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Date, Boolean, ForeignKey, text

from app.auth.auth_models import User, ResearchTopic, ProgrammingLanguage
from app.student.student_models import Major, Course

class Faculty(User):
    __tablename__='faculty'

    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    is_verified: sqlo.Mapped[bool] = sqlo.mapped_column(default=False)
    
    positions: sqlo.WriteOnlyMapped['ResearchPosition'] = relationship(back_populates='faculty')
    #referals: sqlo.WriteOnlyMapped['Application'] = relationship(back_populates='reference')
    __mapper_args__ = {
    'polymorphic_identity': 'Faculty'
    }
    
class ResearchPosition(db.Model):
    __tablename__ = 'research_position'

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

    
    # Foreign key for Faculty who created the position
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    faculty: Mapped[User] = relationship(back_populates="positions")

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
    applications: sqlo.WriteOnlyMapped['Application'] = relationship(back_populates= 'position', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Position {} - Title: {} - {} - Start: {} - End: {} - Size: {} - GPA: {}>'.format(self.id, self.title, self.description, self.start_date, self.end_date, self.team_size, self.min_gpa)

    def get_faculty_name(self):
        first = db.session.scalars(self.faculty.get_firstname()).first()
        last = db.session.scalars(self.faculty.get_lastname()).first()
        return first + ' ' + last
    

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

#an application is connected many-to-one with student and positions
class Application(db.Model):
    __tablename__ = 'application'
    #Primary Key
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    #title: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(200))
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))
    student_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), index=True, nullable=False)
    position_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(ResearchPosition.id), index=True, nullable=False)
    #reference_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.ForeignKey(User.id), index=True)
    statement: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1000), nullable=False)
    
    #Relationships
    #student: sqlo.Mapped[User] = sqlo.relationship(back_populates = 'applications')
    position: sqlo.Mapped[ResearchPosition] = sqlo.relationship(back_populates = 'applications')
    #reference: sqlo.Mapped[Optional[User]] = sqlo.relationship(back_populates = 'referals')

    #Methods
    def __repr__(self):
        return '<Application - {} student: {} - position: {} - reference: {}>'.format(self.id, self.student.get_username(), self.position.title, 
                                                                                      self.reference.get_username)
    def needs_reference(self):
        if self.position.reference_required == True:
            return True
        else:
            return False

