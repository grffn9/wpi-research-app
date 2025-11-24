from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, BooleanField, IntegerField, FloatField, SelectMultipleField, SelectField, FieldList, FormField, widgets, Form)
from wtforms.validators import (ValidationError, DataRequired, EqualTo, Email, NumberRange, Optional)
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


from app import db
import sqlalchemy as sqla
from app.models.models import (Student, Major, ResearchTopic, ProgrammingLanguage, Course, Instructor, Grade, User)

from app.student.student_forms import CourseworkForm, get_courses, get_grades, get_instructors

def get_majors():
    return db.session.scalars(sqla.select(Major).order_by(Major.name)).all()

def get_research_topics():
    return db.session.scalars(sqla.select(ResearchTopic).order_by(ResearchTopic.name)).all()

def get_languages():
    return db.session.scalars(sqla.select(ProgrammingLanguage).order_by(ProgrammingLanguage.name)).all()

class FacultyRegistrationForm(FlaskForm):
   
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


    submit = SubmitField('Register')


    def validate_username(self, username):
        query = sqla.select(User).where(User.username == username.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('The username already exists! Please use a different username.')



class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit= SubmitField('Sign In')


class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])

    gpa = FloatField('Cumulative GPA', validators=[Optional(), NumberRange(min=0.0, max=4.0)])
    majors = QuerySelectMultipleField(
        'Majors',
        query_factory=get_majors,
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    research_topics = QuerySelectMultipleField(
        'Research Topics',
        query_factory=get_research_topics,
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    programming_languages = QuerySelectMultipleField(
        'Programming Languages',
        query_factory=get_languages,
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )

    coursework = FieldList(FormField(CourseworkForm), min_entries=0)

    submit = SubmitField('Register')

    def validate_username(self, username):
        query = sqla.select(User).where(User.username == username.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('That username already exists! Please use a different username.')

    def validate_email(self, email):
        query = sqla.select(User).where(User.email == email.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('That email is already registered. Please use a different email address.')

    def validate_wpi_id(self, wpi_id):
        query = sqla.select(Student).where(Student.wpi_id == wpi_id.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('That WPI ID is already registered.')

