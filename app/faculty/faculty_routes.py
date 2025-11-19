# /faculty/profile
import sys
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from app.faculty import faculty_blueprint as bp_faculty

# @bp_faculty.route('/', methods=['GET'])
@bp_faculty.route('/faculty/profile', methods=['GET'])
def index():
    # empty_form = EmptyForm()
    return render_template('display_profile.html', title = "Display Profile", faculty = current_user)
