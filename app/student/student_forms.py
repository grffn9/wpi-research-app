from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, FieldList, FormField, widgets, Form
from wtforms.validators import  ValidationError, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

from app import db
import sqlalchemy as sqla
# from app.student.student_models import Major, Course, Instructor, Grade
from app.models.models import Major, Course, Instructor, Grade

from app.auth.auth_models import ResearchTopic, ProgrammingLanguage

def get_courses():
    return db.session.scalars(sqla.select(Course).order_by(Course.coursenum)).all()

def get_instructors():
    return db.session.scalars(sqla.select(Instructor).order_by(Instructor.name)).all()

def get_grades():
    return db.session.scalars(sqla.select(Grade).order_by(Grade.value)).all()

class CourseworkForm(Form):
    course = QuerySelectField(
        'Advanced Course',
        query_factory=get_courses,
        get_label=lambda c: f"{c.coursenum} - {c.title}",
        allow_blank=False
    )
    grade = QuerySelectField(
        'Grade Earned',
        query_factory=get_grades,
        get_label='value',
        allow_blank=False
    )
    instructor = QuerySelectField(
        'Instructor',
        query_factory=get_instructors,
        get_label='name',
        allow_blank=False
    )



class EditProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])
    gpa = FloatField('GPA')
    
    majors = QuerySelectMultipleField(
        'Majors',
        query_factory=lambda: db.session.scalars(sqla.select(Major)).all(),
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    research_topics = QuerySelectMultipleField(
        'Research Topics',
        query_factory=lambda: db.session.scalars(sqla.select(ResearchTopic)).all(),
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    programming_languages = QuerySelectMultipleField(
        'Programming Languages',
        query_factory=lambda: db.session.scalars(sqla.select(ProgrammingLanguage)).all(),
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    
    coursework = FieldList(FormField(CourseworkForm), min_entries=0)
    
    submit = SubmitField('Update Profile')