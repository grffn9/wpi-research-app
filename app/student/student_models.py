from typing import Optional, List
from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from app.auth.auth_models import User

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
    department : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))
    
    courses : sqlo.WriteOnlyMapped['Course'] = sqlo.relationship(back_populates= 'major')
    students_in_major : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
        secondary=students_majors_table,
        back_populates='majors_of_student',
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
    majors_of_student : sqlo.WriteOnlyMapped['Major'] = sqlo.relationship(
        secondary=students_majors_table,
        back_populates='students_in_major',
    )
    
    research_topics : sqlo.WriteOnlyMapped['ResearchTopic'] = sqlo.relationship(
        secondary=student_research_topics,
    )
    
    programming_languages : sqlo.WriteOnlyMapped['ProgrammingLanguage'] = sqlo.relationship(
        secondary=student_programming_languages,
    )
    
    coursework : sqlo.WriteOnlyMapped['StudentCourse'] = sqlo.relationship(back_populates='student')

    def __repr__(self):
        return '<Student {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)

    def get_majors(self):
        query = self.majors_of_student.select()
        return db.session.scalars(query).all()