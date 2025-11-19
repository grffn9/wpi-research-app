import sys
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sqla

from app import db
from app.student.student_models import Post
from app.faculty.faculty_models import ResearchPosition
from app.student.student_forms import PostForm

from app.student import student_blueprint as bp_student

# @bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET'])
def index():
    all_positions = db.session.scalars(sqla.select(ResearchPosition))
    # all_posts  = positions.all()     
    return render_template('index.html', title="Research Application Portal", positions=all_positions)
