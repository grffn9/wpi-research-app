import sys
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import sqlalchemy as sqla

from app import db

from app.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('student_index.html')

@bp_student.route('/profile', methods=['GET'])
@login_required
def profile():
    if current_user.user_type != 'Student':
        flash('Access denied. You must be a student to view this page.')
        return redirect(url_for('student.index'))
    return render_template('profile.html')
