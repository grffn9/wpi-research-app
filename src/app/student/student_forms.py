from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, SelectField, IntegerField, FloatField, FieldList, FormField, widgets, Form, TextAreaField
from wtforms.validators import  ValidationError, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

from app import db
import sqlalchemy as sqla
from app.models.models import Major, Course, Instructor, Grade,  ResearchTopic, ProgrammingLanguage, Faculty


def get_courses():
    return db.session.scalars(sqla.select(Course).order_by(Course.coursenum)).all()

def get_instructors():
    return db.session.scalars(sqla.select(Instructor).order_by(Instructor.name)).all()

def get_grades():
    return db.session.scalars(sqla.select(Grade).order_by(Grade.value)).all()

def get_faculty():
    return db.session.scalars(sqla.select(Faculty).order_by(Faculty.lastname)).all()

class ApplicationForm(FlaskForm):
    statement = TextAreaField('Statement of Interest', validators=[DataRequired()])
    reference = QuerySelectField(
        'Faculty Reference (Optional)',
        query_factory=get_faculty,
        get_label=lambda f: f"{f.firstname} {f.lastname}",
        allow_blank=True
    )
    submit = SubmitField('Apply')

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

class SortForm(FlaskForm):
    recommended = BooleanField('Recommended Positions', default=False)
    submit = SubmitField("Refresh")
