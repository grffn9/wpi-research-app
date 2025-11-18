import sys
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sqla

from app import db
from app.student.student_models import Post
from app.student.student_forms import PostForm

from app.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/index', methods=['GET'])
def index():
    posts = db.session.scalars(sqla.select(Post).order_by(Post.timestamp.desc()))
    all_posts  = posts.all()     
    return render_template('index.html', title="Smile Portal", posts=all_posts)
