from config import Config
from app.auth.auth_models import User
from app.faculty.faculty_models import Faculty
from app.student.student_models import (
    Major,
    ResearchTopic,
    ProgrammingLanguage,
    Course,
    Instructor,
    Grade,
)
from app import create_app, db, mail
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {
        'sqla': sqla,
        'sqlo': sqlo,
        'db': db,
        'user': User,
        'faculty': Faculty,
        'major': Major,
        'course': Course,
        'grade': Grade,
    }


@sqla.event.listens_for(Faculty.__table__, 'after_create')
def add_faculty(*args, **kwargs):
    query = sqla.select(Faculty)
    if db.session.scalars(query).first() is None:
        faculty_members = [
        {'firstname':'John','lastname':'Doe', 'email':'john.doe@example.com', 'is_verified': True},
          {'firstname':'Jane','lastname':'Smith','email':'jane.smith@example.com', 'is_verified': False},
          {'firstname':'Jim','lastname':'Brown','email':'jim.brown@example.com', 'is_verified': False},
          {'firstname':'Harry','lastname':'Davis','email':'harry.davis@example.com', 'is_verified': False}, 
          {'firstname':'Lisa','lastname':'Wilson','email':'lisa.wilson@example.com', 'is_verified': False}  ]
        for m in faculty_members:
            db.session.add(Faculty(firstname = m['firstname'], lastname = m['lastname'], email = m['email'], is_verified = m['is_verified']))
        john = db.session.scalars(sqla.select(Faculty).where(Faculty.email == 'john.doe@example.com')).first()


@sqla.event.listens_for(Major.__table__, 'after_create')
def add_majors(*args, **kwargs):
    query = sqla.select(Major)
    if db.session.scalars(query).first() is None:
        majors = [
            {'name': 'Computer Science', 'department': 'Computer Science'},
            {'name': 'Data Science', 'department': 'Mathematical Sciences'},
            {'name': 'Robotics Engineering', 'department': 'Robotics Engineering'},
            {'name': 'Electrical Engineering', 'department': 'Electrical & Computer Engineering'},
        ]
        for m in majors:
            db.session.add(Major(name=m['name'], department=m['department']))
        db.session.commit()


@sqla.event.listens_for(ResearchTopic.__table__, 'after_create')
def add_research_topics(*args, **kwargs):
    query = sqla.select(ResearchTopic)
    if db.session.scalars(query).first() is None:
        topics = [
            {'name': 'Artificial Intelligence'},
            {'name': 'Machine Learning'},
            {'name': 'Cybersecurity'},
            {'name': 'Human-Computer Interaction'},
            {'name': 'Data Visualization'},
        ]
        for t in topics:
            db.session.add(ResearchTopic(name=t['name']))
        db.session.commit()


@sqla.event.listens_for(ProgrammingLanguage.__table__, 'after_create')
def add_programming_languages(*args, **kwargs):
    query = sqla.select(ProgrammingLanguage)
    if db.session.scalars(query).first() is None:
        languages = [
            {'name': 'Python'},
            {'name': 'Java'},
            {'name': 'C++'},
            {'name': 'Rust'},
            {'name': 'JavaScript'},
        ]
        for l in languages:
            db.session.add(ProgrammingLanguage(name=l['name']))
        db.session.commit()


@sqla.event.listens_for(Grade.__table__, 'after_create')
def add_grades(*args, **kwargs):
    query = sqla.select(Grade)
    if db.session.scalars(query).first() is None:
        grades = [{'value': 'A'}, {'value': 'A-'}, {'value': 'B+'}, {'value': 'B'}]
        for g in grades:
            db.session.add(Grade(value=g['value']))
        db.session.commit()


@sqla.event.listens_for(Instructor.__table__, 'after_create')
def add_instructors(*args, **kwargs):
    query = sqla.select(Instructor)
    if db.session.scalars(query).first() is None:
        instructors = [
            {'name': 'Dr. Griffin Munhall'},
            {'name': 'Dr. Craig Shue'},
            {'name': 'Dr. Matthew Ahrens'},
        ]
        for i in instructors:
            db.session.add(Instructor(name=i['name']))
        db.session.commit()


@sqla.event.listens_for(Course.__table__, 'after_create')
def add_courses(*args, **kwargs):
    query = sqla.select(Course)
    if db.session.scalars(query).first() is None:
        catalog = [
            {'coursenum': 'CS 500', 'title': 'Advanced Algorithms', 'major_name': 'Computer Science'},
            {'coursenum': 'DS 550', 'title': 'Statistical Learning Theory', 'major_name': 'Data Science'},
            {'coursenum': 'RBE 521', 'title': 'Robot Dynamics', 'major_name': 'Robotics Engineering'},
            {'coursenum': 'ECE 531', 'title': 'Embedded Systems', 'major_name': 'Electrical Engineering'},
        ]
        majors_by_name = {
            major.name: major
            for major in db.session.scalars(sqla.select(Major)).all()
        }
        for c in catalog:
            major = majors_by_name.get(c['major_name'])
            if major is None:
                continue
            db.session.add(
                Course(
                    coursenum=c['coursenum'],
                    title=c['title'],
                    major=major,
                )
            )
        db.session.commit()


@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)