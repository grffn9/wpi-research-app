######################################################
#AUTH
######################################################

from datetime import datetime, date, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Date, Boolean, ForeignKey, text
from app import db


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(db.Model,UserMixin):
    __tablename__='user'
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), index = True, unique = True, nullable=True)
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True)
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    password_hash : sqlo.Mapped[Optional[str]] =sqlo.mapped_column(sqla.String(256))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
    'polymorphic_identity': 'User',
    'polymorphic_on': user_type
    }

    def __repr__(self):
        return '<User {} {} - {} - {} - {}>'.format(self.firstname, self.lastname, self.username, self.email, self.user_type)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_firstname(self):
        return self.firstname
    
    def get_lastname(self):
        return self.lastname
    
    def get_email(self):
        return self.email

    def get_username(self):
        return self.username
    
class ResearchTopic(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100), unique=True)
    
    def __repr__(self):
        return self.name
    
class ProgrammingLanguage(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100), unique=True)

    def __repr__(self):
        return self.name
    



######################################################
#Faculty
######################################################




from datetime import datetime, date, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo



from datetime import datetime, date, timezone
from typing import Optional, List

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Date, Boolean, ForeignKey, text


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
        ForeignKey("faculty.id"), nullable=False
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
    applications: sqlo.Mapped[List["Application"]] = sqlo.relationship(
        back_populates="position",
        cascade="all, delete-orphan"
    )


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




######################################################
#Student
######################################################

from typing import Optional, List
from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


# Association Tables
student_research_topics = db.Table('student_research_topics',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('research_topic_id', db.Integer, db.ForeignKey('research_topic.id'), primary_key=True)
)

student_programming_languages = db.Table('student_programming_languages',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('programming_language_id', db.Integer, db.ForeignKey('programming_language.id'), primary_key=True)
)

students_majors_table = db.Table(
    'students_majors_table',
    db.metadata,
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key=True),
    sqla.Column('major_id', sqla.Integer, sqla.ForeignKey('major.id'), primary_key=True)
)


class Instructor(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))

    def __repr__(self):
        return self.name

class Grade(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    value : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5), unique=True)

    def __repr__(self):
        return self.value


class Major(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    department : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150), nullable=True)
    
    courses : sqlo.WriteOnlyMapped['Course'] = sqlo.relationship(back_populates= 'major')
    
    students_in_major : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
        secondary=students_majors_table,
        back_populates='majors_of_student',
        passive_deletes=True
    )
    
    def __repr__(self):
        return '<Major  - {} name: {} - department: {}>'.format(self.id,self.name,self.department)
    
    def get_name(self):
        return self.name
    
    def get_department(self):
        return self.department
    
    def get_courses(self):
        query = self.courses.select()
        return db.session.scalars(query).all()
    
    def get_students(self):
        query = self.students_in_major.select()
        return db.session.scalars(query).all()

class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    majorid : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Major.id), index = True)
    coursenum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), index = True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))
    
    major : sqlo.Mapped[Major] = sqlo.relationship(back_populates= 'courses')
    
    def __repr__(self):
        return '<Course id: {} - coursenum: {} - title: {}>'.format(self.id,self.coursenum, self.title)
    
    def get_coursenum(self):
        return self.coursenum
    
    def get_title(self):
        return self.title
    
    def get_major(self):
        return self.major

class StudentCourse(db.Model):
    __tablename__ = 'student_course'
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    student_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('student.id'))
    course_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('course.id'))
    instructor_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('instructor.id'))
    grade_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('grade.id'))
    
    student : sqlo.Mapped['Student'] = sqlo.relationship(back_populates='coursework')
    course : sqlo.Mapped['Course'] = sqlo.relationship()
    instructor : sqlo.Mapped['Instructor'] = sqlo.relationship()
    grade : sqlo.Mapped['Grade'] = sqlo.relationship()

class Student(User):
    __tablename__ = 'student'
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'), primary_key=True)
    wpi_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, unique=True)
    gpa : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'Student',
    }

    # Relationships
    majors_of_student : sqlo.Mapped[List['Major']] = sqlo.relationship(
        secondary=students_majors_table,
        back_populates='students_in_major',
    )
    
    research_topics : sqlo.Mapped[List['ResearchTopic']] = sqlo.relationship(
        secondary=student_research_topics,
    )
    
    programming_languages : sqlo.Mapped[List['ProgrammingLanguage']] = sqlo.relationship(
        secondary=student_programming_languages,
    )
    
    coursework : sqlo.Mapped[List['StudentCourse']] = sqlo.relationship(back_populates='student', cascade="all, delete-orphan")
    
    applications: sqlo.Mapped[List["Application"]] = sqlo.relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )




    def __repr__(self):
        return '<Student {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)

    def get_majors(self):
        return self.majors_of_student

    def get_research_topics(self):
        return self.research_topics

    def get_programming_languages(self):
        return self.programming_languages

    def get_coursework(self):
        return self.coursework
        query = self.coursework.select()
        return db.session.scalars(query).all()


######################################################
#Application
######################################################

#an application is connected many-to-one with student and positions
class Application(db.Model):
    __tablename__ = "application"

    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), default="pending")
    statement: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1000), nullable=False)

    student_id: sqlo.Mapped[int] = sqlo.mapped_column(
        sqla.ForeignKey("student.id"), index=True, nullable=False
    )
    position_id: sqlo.Mapped[int] = sqlo.mapped_column(
        sqla.ForeignKey("research_position.id"), index=True, nullable=False
    )
    reference_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(
        sqla.ForeignKey("faculty.id"), index=True, nullable=True
    )

    # Relationships
    student: sqlo.Mapped[Student] = sqlo.relationship(back_populates="applications")
    position: sqlo.Mapped[ResearchPosition] = sqlo.relationship(back_populates="applications")
    # reference: sqlo.Mapped[Optional["User"]] = sqlo.relationship()


    #Methods
    def __repr__(self):
        return '<Application - {} student: {} - position: {} - reference: {}>'.format(self.id, self.student.get_username(), self.position.title, 
                                                                                      self.reference.get_username)
    def needs_reference(self):
        if self.position.reference_required == True:
            return True
        else:
            return False
