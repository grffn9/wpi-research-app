import sys
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sqla

from app import db
from app.main.models import Post
from app.main.forms import PostForm

from app.main import main_blueprint as bp_main

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    posts = db.session.scalars(sqla.select(Post).order_by(Post.timestamp.desc()))
    all_posts  = posts.all()     
    return render_template('index.html', title="Smile Portal", posts=all_posts)
