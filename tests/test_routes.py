"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.models.models import *
from config import Config
import sqlalchemy as sqla


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_user(uname, uemail,passwd):
    user = User(username=uname, firstname="test", lastname="test", email=uemail)
    user.set_password(passwd)
    return user

def new_faculty(uname, uemail,passwd):
    faculty = Faculty(username=uname, firstname="test", lastname="test", email=uemail, is_verified=True)
    faculty.set_password(passwd)
    return faculty

def new_student(uname, uemail,passwd):
    student = Student(username=uname, firstname="test", lastname="test", email=uemail, wpi_id="123456", gpa=3.5)
    student.set_password(passwd)
    return student

# def init_tags():
#     # check if any tags are already defined in the database
#     count = db.session.scalar(db.select(db.func.count(Tag.id)))
#     print("**************", count)
#     # initialize the tags
#     if count == 0:
#         tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
#         for t in tags:
#             db.session.add(Tag(name=t))
#         db.session.commit()
#     return None

# def init_faculty():
#     users = []
#     faculty_members = [
#         {'firstname':'John','lastname':'Doe', 'email':'john.doe@example.com', 'is_verified': False},
#         {'firstname':'Jane','lastname':'Smith','email':'jane.smith@example.com', 'is_verified': False}]
#     for data in faculty_members:   # fix typo
#         user = User(
#             firstname=data["firstname"],
#             lastname=data["lastname"],
#             email=data["email"],
#             is_verified=True,
#             username=data["firstname"] + data["lastname"]
#         )
#         user.set_password("123")  # hash and store password
#         db.session.add(user)
#         users.append(user)
#     db.session.commit()
#     return users


@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    #add a user    
    user1 = new_student(uname='snow', uemail='snow@wpi.edu', passwd='123')
    user2 = new_faculty(uname='john', uemail='john.doe@example.com', passwd='123')

    # Insert user data
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

# def test_register_page(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/user/register' page is requested (GET)
#     THEN check that the response is valid
#     """
#     # Create a test client using the Flask application configured for testing
#     response = test_client.get('/user/register')
#     assert response.status_code == 200
#     assert b"Register" in response.data

# def test_register(test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/user/register' form is submitted (POST)
#     THEN check that the response is valid and the database is updated correctly
#     """
#     # Create a test client using the Flask application configured for testing
#     response = test_client.post('/user/register', 
#                           data=dict(username='john', email='john@wpi.edu',password="bad-bad-password",password2="bad-bad-password"),
#                           follow_redirects = True)
#     assert response.status_code == 200
    
#     s = db.session.scalars(sqla.select(User).where(User.username == 'john')).first()
#     s_count = db.session.scalar(sqla.select(db.func.count()).where(User.username == 'john'))
    
#     assert s.email == 'john@wpi.edu'
#     assert s_count == 1
#     assert b"Sign In" in response.data   
#     assert b"Please log in to access this page." in response.data

# def test_invalidlogin(test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/user/login' form is submitted (POST) with wrong credentials
#     THEN check that the response is valid and login is refused 
#     """
#     response = test_client.post('/user/login', 
#                           data=dict(username='snow', password='12345',remember_me=False),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Invalid username or password" in response.data

# ------------------------------------
# Helper functions

def do_login_faculty(test_client, path , email, passwd):
    response = test_client.post(path, 
                          data=dict(email=email, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #Students should update this assertion condition according to their own page content
    assert b"Hello Faculty." in response.data

def do_login_student(test_client, path , email, passwd):
    response = test_client.post(path, 
                          data=dict(email=email, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #Students should update this assertion condition according to their own page content
    assert b"Hello Student." in response.data  

def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to login page after logout.
    #Students should update this assertion condition according to their own page content 
    assert b"Sign In" in response.data
    assert b"New User?" in response.data    

# ------------------------------------

# def test_login_logout(request,test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/user/login' form is submitted (POST) with correct credentials
#     THEN check that the response is valid and login is succesfull 
#     """
#     do_login(test_client, path = '/user/login', username = 'snow', passwd = '1234')

#     do_logout(test_client, path = '/user/logout')



def test_list_majors(test_client,init_database):

    # faculty login
    do_login_faculty(test_client, '/user/login', 'john.doe@example.com', '123')

    response = test_client.get('/faculty/majors', follow_redirects=True)
    assert response.status_code == 200
    assert b"Majors" in response.data
    do_logout(test_client, path = '/user/logout')

    # student login
    do_login_student(test_client, '/user/login', 'snow@wpi.edu', '123')
    
    response = test_client.get('/faculty/majors', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')



def test_create_major(test_client,init_database):
 #first login
    do_login_faculty(test_client, '/user/login', 'john.doe@example.com', '123')
    
    #test the create major form 
    response = test_client.get('/faculty/majors/create')
    assert response.status_code == 200
    assert b"Create Major" in response.data 

    
    #test posting a major
    response = test_client.post('/faculty/majors/create', 
                          data=dict(name = 'test', department = 'Testing Department'),  
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"test" in response.data
    assert b"Testing Department" in response.data 

    m  = db.session.scalars(sqla.select(Major).where(Major.name == 'test').where(Major.department == "Testing Department")).first()
    m_count = db.session.scalar(sqla.select(db.func.count()).where(Major.name == 'test').where(Major.department == "Testing Department"))
    assert m.get_name() == 'test'
    assert m_count == 1

    do_logout(test_client, path = '/user/logout')

    # student login
    do_login_student(test_client, '/user/login', 'snow@wpi.edu', '123')
    
    response = test_client.get('/faculty/majors/create', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')


def test_edit_major(test_client,init_database):
 #first login
    do_login_faculty(test_client, '/user/login', 'john.doe@example.com', '123')

    major = Major(name="test", department="Testing Department")
    db.session.add(major)
    db.session.commit()

    
    #test the create major form 
    response = test_client.get('/faculty/majors/1/edit')
    assert response.status_code == 200
    assert b"Edit Major" in response.data 

    #get current values
    response = test_client.get('/faculty/majors/1/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b"test" in response.data
    assert b"Testing Department" in response.data

    #edit values
    response = test_client.post('/faculty/majors/1/edit', 
                          data=dict(name = 'new name', department = 'new Department'),  
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"new name" in response.data
    assert b"new Department" in response.data 
    m  = db.session.scalars(sqla.select(Major).where(Major.name == 'new name').where(Major.department == "new Department")).first()
    m_count = db.session.scalar(sqla.select(db.func.count()).where(Major.name == 'new name').where(Major.department == "new Department"))
    old_m_count = db.session.scalar(sqla.select(db.func.count()).where(Major.name == 'test').where(Major.department == "Testing Department"))

    all_majors = db.session.scalars(sqla.select(Major)).all()
    assert len(all_majors) == 1
    assert old_m_count == 0
    assert m.get_name() == 'new name'
    assert m_count == 1

    do_logout(test_client, path = '/user/logout')

    # student login
    do_login_student(test_client, '/user/login', 'snow@wpi.edu', '123')
    
    response = test_client.get('/faculty/majors/1/edit', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')





def test_delete_major(test_client,init_database):
 #first login
    do_login_faculty(test_client, '/user/login', 'john.doe@example.com', '123')

    major = Major(name="test", department="Testing Department")
    db.session.add(major)
    db.session.commit()

    
    #get the major  
    response = test_client.get('/faculty/majors')
    assert response.status_code == 200
    assert b"test" in response.data 

    #delete the major
    response = test_client.post('/faculty/majors/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"Major deleted." in response.data



    m  = db.session.scalars(sqla.select(Major).where(Major.name == 'test').where(Major.department == "Testing Department")).first()
    m_count = db.session.scalar(sqla.select(db.func.count()).where(Major.name == 'test').where(Major.department == "Testing Department"))
    all_majors = db.session.scalars(sqla.select(Major)).all()

    assert len(all_majors) == 0
    assert m is None
    assert m_count == 0

    do_logout(test_client, path = '/user/logout')

    # student login
    do_login_student(test_client, '/user/login', 'snow@wpi.edu', '123')
    
    response = test_client.get('/faculty/majors/1/edit', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')



def test_list_topics(test_client,init_database):

    # faculty login
    do_login_faculty(test_client, '/user/login', 'john.doe@example.com', '123')

    response = test_client.get('/faculty/topics', follow_redirects=True)
    assert response.status_code == 200
    assert b"Research Topics" in response.data
    do_logout(test_client, path = '/user/logout')

    # student login
    do_login_student(test_client, '/user/login', 'snow@wpi.edu', '123')

    response = test_client.get('/faculty/topics', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')


