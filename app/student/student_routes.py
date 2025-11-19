import sys
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import sqlalchemy as sqla

from app import db

from app.faculty.faculty_models import ResearchPosition
from app.student.student_forms import PostForm

from app.student import student_blueprint as bp_student

# @bp_student.route('/', methods=['GET'])
@bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET'])
@login_required
def index():
    all_positions = db.session.scalars(sqla.select(ResearchPosition)).all()
    return render_template('student_index.html', title="Research Application Portal", positions=all_positions)

@bp_student.route('/profile', methods=['GET'])
@login_required
def profile():
    if current_user.user_type != 'Student':
        flash('Access denied. You must be a student to view this page.')
        return redirect(url_for('student.index'))
    return render_template('profile.html')
    

