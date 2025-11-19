import sys
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sqla

from app import db

from app.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html')
