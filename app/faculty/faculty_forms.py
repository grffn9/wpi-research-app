from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,BooleanField, SelectMultipleField, DateField, widgets
from wtforms.validators import  ValidationError, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from datetime import datetime
# from app.faculty.faculty_models import Major, Course
from app.models.models import Major, Course, ResearchTopic, ProgrammingLanguage
from wtforms.validators import ValidationError, DataRequired
from app import db
import sqlalchemy as sqla

class ResearchPositionForm(FlaskForm):
    # Basic fields
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])

    start_date = DateField("Start Date (YYYY-MM-DD)", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("End Date (YYYY-MM-DD)", format="%Y-%m-%d", validators=[DataRequired()])

    team_size = IntegerField("Team Size", validators=[DataRequired()])
    min_gpa = FloatField("Minimum GPA", validators=[DataRequired()])
    reference_required = BooleanField("Reference Required?")

    preferred_majors = QuerySelectMultipleField(
        'Preferred Majors',
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

    required_courses = QuerySelectMultipleField(
        'Required Courses',
        query_factory=lambda: db.session.scalars(sqla.select(Course)).all(),
        get_label='title',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )

    submit = SubmitField("Save Position")

    # Validators
    def validate_end_date(self, field):
        if self.start_date.data and field.data < self.start_date.data:
            raise ValidationError("End date cannot be before start date.")

    def validate_min_gpa(self, field):
        if field.data < 0 or field.data > 4.0:
            raise ValidationError("GPA must be between 0.0 and 4.0.")

class AddItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add")

# class UpdatetemForm(FlaskForm):
#     name = StringField("Name", validators=[DataRequired()])
#     submit = SubmitField("Add")

# class DeleteItemForm(FlaskForm):
#     name = StringField("Name", validators=[DataRequired()])
#     submit = SubmitField("Add")
