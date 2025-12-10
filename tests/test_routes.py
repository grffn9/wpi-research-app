"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import pytest
from app import create_app, db
from app.models.models import User, Student, Faculty, ResearchPosition, Application, Major, ResearchTopic, ProgrammingLanguage, Course, Instructor, Grade, StudentCourse
from config import Config
import sqlalchemy as sqla
from datetime import datetime, date

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

@pytest.fixture
def init_database():
    db.create_all()
    
    m1 = Major(name="Computer Science")
    t1 = ResearchTopic(name="AI")
    l1 = ProgrammingLanguage(name="Python")
    c1 = Course(coursenum="CS101", title="Intro to CS", major=m1)
    i1 = Instructor(name="Prof. Smith")
    g1 = Grade(value="A")
    
    db.session.add_all([m1, t1, l1, c1, i1, g1])
    db.session.commit()
    
    f1 = Faculty(username='faculty1', email='faculty1@wpi.edu', firstname='Fac', lastname='Ulty')
    f1.set_password('password')
    f1.is_verified = True
    db.session.add(f1)
    db.session.commit()
    
    s1 = Student(username='student1', email='student1@wpi.edu', firstname='Stu', lastname='Dent', wpi_id=123456789)
    s1.set_password('password')
    db.session.add(s1)
    db.session.commit()
    
    p1 = ResearchPosition(
        title="AI Research",
        description="Doing AI stuff",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 5, 1),
        team_size=2,
        min_gpa=3.0,
        faculty_id=f1.id,
        reference_required=False
    )
    db.session.add(p1)
    db.session.commit()

    yield

    db.drop_all()

def login_student(test_client):
    return test_client.post('/user/login',
        data=dict(email='student1@wpi.edu', password='password'),
        follow_redirects=True
    )

def test_student_index(test_client, init_database):
    login_student(test_client)
    response = test_client.get('/student/index')
    assert response.status_code == 200
    assert b"AI Research" in response.data

def test_student_profile(test_client, init_database):
    login_student(test_client)
    response = test_client.get('/profile')
    
    assert response.status_code == 200
    assert b"Stu" in response.data 
    assert b"Dent" in response.data

def test_edit_profile(test_client, init_database):
    login_student(test_client)
    
    response = test_client.get('/edit_profile')
    assert response.status_code == 200
    
    m1 = db.session.scalars(sqla.select(Major)).first()
    
    response = test_client.post('/edit_profile', data={
        'firstname': 'Student',
        'lastname': 'Updated',
        'username': 'student1',
        'email': 'student1@wpi.edu',
        'wpi_id': 123456789,
        'gpa': 3.8,
        'majors': [m1.id],
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    s1 = db.session.scalars(sqla.select(Student).where(Student.username == 'student1')).first()
    assert s1.lastname == 'Updated'
    assert s1.gpa == 3.8

def test_apply(test_client, init_database):
    login_student(test_client)
    p1 = db.session.scalars(sqla.select(ResearchPosition)).first()
    
    response = test_client.get(f'/apply/{p1.id}')
    assert response.status_code == 200
    
    response = test_client.post(f'/apply/{p1.id}', data={
        'statement': 'I am very interested.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Application submitted successfully!" in response.data
    
    app = db.session.scalars(sqla.select(Application)).first()
    
    assert app is not None
    assert app.position_id == p1.id
    assert app.statement == 'I am very interested.'

def test_withdraw_application(test_client, init_database):
    login_student(test_client)
    p1 = db.session.scalars(sqla.select(ResearchPosition)).first()
    s1 = db.session.scalars(sqla.select(Student).where(Student.username == 'student1')).first()
    
    app = Application(student_id=s1.id, position_id=p1.id, statement="Test", status='pending')
    db.session.add(app)
    db.session.commit()
    
    response = test_client.post(f'/withdraw_application/{app.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Application has been withdrawn." in response.data
    
    app_check = db.session.get(Application, app.id)
    assert app_check is None
    
