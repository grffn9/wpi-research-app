import sys
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

import sqlalchemy as sqla

from app import db


from app.faculty import faculty_blueprint as bp_faculty
@bp_faculty.route('/', methods=['GET'])
@bp_faculty.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title="Research Portal")
