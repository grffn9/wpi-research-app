"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
from turtle import pos
import pytest
from app import create_app, db
from app.models.models import User, Student, Faculty, ResearchPosition, Application, Major, ResearchTopic, ProgrammingLanguage, Course, Instructor, Grade, StudentCourse
from config import Config
import sqlalchemy as sqla
from datetime import datetime, date, timedelta


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
    
    m1 = Major(name="Computer Science", department="CS Dept")
    t1 = ResearchTopic(name="AI")
    l1 = ProgrammingLanguage(name="Python")
    c1 = Course(coursenum="CS101", title="Intro to CS", major=m1)
    i1 = Instructor(name="Prof. Smith")
    g1 = Grade(value="A")
    
    db.session.add_all([m1, t1, l1, c1, i1, g1])
    db.session.commit()
    
    f1 = Faculty(username='faculty1', email='faculty1@wpi.edu', firstname='Fac', lastname='Ulty', is_verified=True)
    f1.set_password('password')
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

def login_faculty(test_client):
    return test_client.post('/user/login',
        data=dict(email='faculty1@wpi.edu', password='password'),
        follow_redirects=True
    )

def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"New User?" in response.data    


def test_student_index(test_client, init_database):
    login_student(test_client)
    response = test_client.get('/student/index')
    assert response.status_code == 200
    assert b"AI Research" in response.data
    do_logout(test_client, path = '/user/logout')

def test_student_profile(test_client, init_database):
    login_student(test_client)
    response = test_client.get('/profile')
    
    assert response.status_code == 200
    assert b"Stu" in response.data 
    assert b"Dent" in response.data
    do_logout(test_client, path = '/user/logout')

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
    do_logout(test_client, path = '/user/logout')


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
    do_logout(test_client, path = '/user/logout')


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
    do_logout(test_client, path = '/user/logout')

    
def test_list_majors(test_client,init_database):

    # faculty login
    login_faculty(test_client)

        
    response = test_client.get('/faculty/majors')
    assert response.status_code == 200
    assert b"Majors" in response.data
    do_logout(test_client, path = '/user/logout')

    # student login
    login_student(test_client)
    
    response = test_client.get('/faculty/majors', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')



def test_create_major(test_client,init_database):
 #first login
    login_faculty(test_client)
    
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
    login_student(test_client)
    
    response = test_client.get('/faculty/majors/create', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')


def test_edit_major(test_client,init_database):
 #first login
    login_faculty(test_client)

    #get current values
    response = test_client.get('/faculty/majors/1/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b"Edit Major" in response.data 
    assert b"Computer Science" in response.data
    assert b"CS Dept" in response.data


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
    login_student(test_client)
    
    response = test_client.get('/faculty/majors/1/edit', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')





def test_delete_major(test_client,init_database):
 #first login
    login_faculty(test_client)

   
    #get the major  
    response = test_client.get('/faculty/majors')
    assert response.status_code == 200
    assert b"Computer Science" in response.data
    assert b"CS Dept" in response.data

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
    login_student(test_client)
    
    response = test_client.get('/faculty/majors/1/edit', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')



def test_list_topics(test_client,init_database):

    # faculty login
    login_faculty(test_client)

    response = test_client.get('/faculty/topics', follow_redirects=True)
    assert response.status_code == 200
    assert b"Research Topics" in response.data
    do_logout(test_client, path = '/user/logout')

    # student login
    login_student(test_client)

    response = test_client.get('/faculty/topics', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')



def test_create_position_get(test_client, init_database):
    login_faculty(test_client)

    response = test_client.get('/create_position')

    assert response.status_code == 200
    do_logout(test_client, path = '/user/logout')

def test_create_position_post(test_client, init_database):
    login_faculty(test_client)

    response = test_client.post(
    "/create_position",
    data= dict(
        title="Test Position",
        description="Research work",
        start_date=(date.today() + timedelta(days=1)).isoformat(),
        end_date=(date.today() + timedelta(days=30)).isoformat(),
        team_size=2,
        min_gpa=3.2,
        reference_required=True,
        preferred_majors=["1"],
        research_topics=["1"],
        programming_languages=["1"],
        required_courses=["1"],
    ),
    follow_redirects=True,
)

    assert response.status_code == 200

    all_pos = db.session.scalars(sqla.select(ResearchPosition)).all()
    assert len(all_pos) == 2  

    pos = db.session.scalars(
        sqla.select(ResearchPosition).where(ResearchPosition.title == 'Test Position')
    ).first()

    assert pos is not None


def test_create_position_bad_start_date(test_client, init_database):
    login_faculty(test_client)
    payload = dict(
        title='Bad Date',
        start_date=date.today() - timedelta(days=1)
    )

    response = test_client.post(
        '/create_position',
        data=payload,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Start date cannot be in the past", "danger" in response.data
    


def test_edit_position(test_client, init_database):
    login_faculty(test_client)

    response = test_client.post('/position/1/edit', 
                          data=dict(title = 'Edit Me', description = 'Test'),  
                          follow_redirects = True)

    assert response.status_code == 200
    assert b"Edit Me" in response.data


def test_faculty_index(test_client, init_database):

    login_faculty(test_client)

    response = test_client.get('/faculty/index')

    assert response.status_code == 200
    assert b"Hello Faculty." in response.data


def test_faculty_profile(test_client, init_database):
    login_faculty(test_client)

    response = test_client.get('/faculty/profile')

    assert response.status_code == 200



def test_view_applicants(test_client, init_database):
    faculty = login_faculty(test_client)

    pos = ResearchPosition(
        title='Applicants',
        description='Test',
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        team_size=1,
        min_gpa=0.0,
        reference_required=False,         
        faculty = db.session.scalars(
        sqla.select(Faculty).where(Faculty.email == 'faculty1@wpi.edu')
        ).first()
    )
    
    db.session.add(pos)
    db.session.commit()

    response = test_client.get(f'/position/{pos.id}/applicants')

    assert response.status_code == 200
    do_logout(test_client, path = '/user/logout')




def test_update_application_status(test_client, init_database):
    login_faculty(test_client)

    sqla.select(Faculty).where(Faculty.username == 'faculty')

    faculty = db.session.scalars(
        sqla.select(Faculty).where(Faculty.email == 'faculty1@wpi.edu')
    ).first()
    do_logout(test_client, path = '/user/logout')

    login_student(test_client)
    student = Student(
        username="student2",
        email="s1@wpi.edu",
        firstname="Stu",
        lastname="Dent",
        wpi_id=999999999
    )
    student.set_password("1234")
    db.session.add(student)
    db.session.commit()
    do_logout(test_client, path = '/user/logout')

    login_faculty(test_client)

    position = ResearchPosition(
        title="Applicants",
        description="test",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        team_size=1,
        min_gpa=0.0,
        reference_required=False,
        faculty=faculty
    )

    

    position = ResearchPosition(
        title="Applicants",
        description="test",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        team_size=1,
        min_gpa=0.0,
        reference_required=False,
        faculty=faculty
    )
    db.session.add(position)
    db.session.commit()

    app_obj = Application(
        student_id=student.id,
        position_id=position.id,
        reference_id=faculty.id,
        reference_status='Pending',
        statement="test statement"
    )
    db.session.add(app_obj)
    db.session.commit()

    response = test_client.post(
        f'/faculty/{app_obj.id}/recommend',
        data=dict(rec_status='Approved'),
        follow_redirects=True
    )

    assert response.status_code == 200
    do_logout(test_client, path = '/user/logout')
#--------------------------------------------------------
def test_list_courses(test_client,init_database):
    #login
    login_faculty(test_client)

    response = test_client.get('/faculty/courses', follow_redirects=True)
    assert response.status_code == 200
    assert b"Courses" in response.data
    do_logout(test_client, path = '/user/logout')

    # student login
    login_student(test_client)

    response = test_client.get('/faculty/courses', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')


def test_create_course(test_client, init_database):
    #login
    login_faculty(test_client)

    #test create_language route
    response = test_client.get('/faculty/courses/create')
    assert response.status_code == 200
    assert b"Create Course" in response.data 

    #test creating language
    response = test_client.post('/faculty/courses/create',
                                data=dict(coursenum="CS 550", title="Foundations of Computer Science", 
                                           major = db.session.scalars(sqla.select(Major)).first()),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Create Course" in response.data
    assert b"CS 550" in response.data 
    assert b"Foundations of Computer Science" in response.data
    #print("|******************************|", response.data)
    c = db.session.scalars(sqla.select(Course).where(Course.coursenum == "CS 550")).first()
    #print("|******************************|", c)
    c_count = db.session.scalar(sqla.select(db.func.count()).where(Course.coursenum == "CS 550"))
    all_courses = db.session.scalars(sqla.select(Course)).all()
    for course in all_courses:
        print("|******************************|", course)
    print("--------------------------------")

    assert c.coursenum == 'CS 550'
    assert c_count == 1
    
    #logout faculty and login student
    do_logout(test_client, path = '/user/logout')
    login_student(test_client)

    response = test_client.get('/faculty/courses/create', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')

def test_edit_courses(test_client, init_database):
    #login 
    login_faculty(test_client)

    response = test_client.get('/faculty/courses/1/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b"Edit Course" in response.data 
    assert b"CS101" in response.data
    assert b"Intro to CS" in response.data
    old_id = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS101'))

    #Edit Values
    response = test_client.post('/faculty/courses/1/edit', 
                          data=dict(coursenum="new course num", 
                                    title="new course name", 
                                    major = db.session.scalars(sqla.select(Major)).first()),  
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"new course num" in response.data
    assert b"new course name" in response.data

    c  = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'new course num')).first()
    c_count = db.session.scalar(sqla.select(db.func.count()).where(Course.coursenum == 'new course num'))
    old_c_count = db.session.scalar(sqla.select(db.func.count()).where(Course.coursenum == 'CS101'))
    print("|******************************|", c)

    all_courses = db.session.scalars(sqla.select(Course)).all() 
    for course in all_courses:
        print("|******************************|", course)
    assert len(all_courses) == 1
    assert c_count == 1
    assert old_c_count == 0
    
    assert c.coursenum == 'new course num'
    assert c.title == 'new course name'
    

    do_logout(test_client, path = '/user/logout')

    # student login
    login_student(test_client)
    
    response = test_client.get('/faculty/courses/1/edit', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')

def test_list_lang(test_client,init_database):
    #login
    login_faculty(test_client)

    response = test_client.get('/faculty/languages', follow_redirects=True)
    assert response.status_code == 200
    assert b"Programming Languages" in response.data
    do_logout(test_client, path = '/user/logout')

    # student login
    login_student(test_client)

    response = test_client.get('/faculty/languages', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')


def test_create_lang(test_client, init_database):
    #login
    login_faculty(test_client)

    #test create_language route
    response = test_client.get('/faculty/languages/create')
    assert response.status_code == 200
    assert b"Programming Language" in response.data #*add what the page returns

    #test creating language
    response = test_client.post('/faculty/languages/create',
                                data=dict(name = "Ruby"),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Ruby" in response.data
    l = db.session.scalars(sqla.select(ProgrammingLanguage).where(ProgrammingLanguage.name == "Ruby")).first()
    lcount = db.session.scalar(sqla.select(db.func.count()).where(ProgrammingLanguage.name == "Ruby"))

    assert l.name == 'Ruby'
    assert lcount == 1
    
    #logout faculty and login student
    do_logout(test_client, path = '/user/logout')
    login_student(test_client)

    response = test_client.get('/faculty/languages/create', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')

def test_edit_language(test_client, init_database):
    #login 
    login_faculty(test_client)

    response = test_client.get('/faculty/languages/1/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b"Edit Programming Language" in response.data 
    assert b"Python" in response.data

    #Edit Values
    response = test_client.post('/faculty/languages/1/edit', 
                          data=dict(name = 'new lang'),  
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"new lang" in response.data
    l  = db.session.scalars(sqla.select(ProgrammingLanguage).where(ProgrammingLanguage.name == 'new lang')).first()
    lcount = db.session.scalar(sqla.select(db.func.count()).where(ProgrammingLanguage.name == 'new lang'))
    old_lcount = db.session.scalar(sqla.select(db.func.count()).where(ProgrammingLanguage.name == 'Python'))

    all_langs = db.session.scalars(sqla.select(ProgrammingLanguage)).all() 
    assert len(all_langs) == 1
    assert old_lcount == 0
    assert l.name == 'new lang'
    assert lcount == 1

    do_logout(test_client, path = '/user/logout')

    # student login
    login_student(test_client)
    
    response = test_client.get('/faculty/languages/1/edit', follow_redirects=True)
    assert response.status_code == 403
    do_logout(test_client, path = '/user/logout')

