from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
# from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError
# from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
# from wtforms.widgets import ListWidget, CheckboxInput
# from flask_login import current_user
# import sqlalchemy as sqla

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')