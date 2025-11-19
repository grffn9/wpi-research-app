from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,BooleanField, SelectMultipleField, DateField
from wtforms.validators import  ValidationError, DataRequired
from datetime import datetime
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

    # Many-to-many (populated dynamically in the view)
    preferred_majors = SelectMultipleField("Preferred Majors", coerce=int)
    research_topics = SelectMultipleField("Research Topics", coerce=int)
    programming_languages = SelectMultipleField("Programming Languages", coerce=int)
    required_courses = SelectMultipleField("Required Courses", coerce=int)

    submit = SubmitField("Save Position")

    # Validators
    def validate_end_date(self, field):
        if self.start_date.data and field.data < self.start_date.data:
            raise ValidationError("End date cannot be before start date.")

    def validate_min_gpa(self, field):
        if field.data < 0 or field.data > 4.0:
            raise ValidationError("GPA must be between 0.0 and 4.0.")