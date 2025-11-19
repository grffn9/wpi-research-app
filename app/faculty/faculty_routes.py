# /faculty/profile
import sys
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sqla

from app import db
from app.faculty.faculty_models import ResearchPosition
from app.faculty.faculty_forms import EmptyForm
from flask_login import login_user, current_user, logout_user, login_required
from app.faculty import faculty_blueprint as bp_faculty

@bp_faculty.route('/', methods=['GET'])
@bp_faculty.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title="Research Portal")

@bp_faculty.route('/', methods=['GET'])
@bp_faculty.route('/faculty/profile', methods=['GET'])
def viewProfile():
    # empty_form = EmptyForm()
    return render_template('display_profile.html', title = "Display Profile", faculty = current_user)
