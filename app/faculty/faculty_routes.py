# /faculty/profile
import sys
from flask import render_template, flash, redirect, url_for, abort, request
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

import sqlalchemy as sqla

import sqlalchemy as sqla
from datetime import datetime
from flask_login import current_user, login_required
from app.faculty.faculty_models import ResearchPosition
from app.faculty.faculty_forms import ResearchPositionForm
from app import db
from app.faculty.faculty_models import ResearchPosition
# from app.faculty.faculty_forms import EmptyForm
from flask_login import login_user, current_user, logout_user, login_required
from app.faculty import faculty_blueprint as bp_faculty
from app.faculty.faculty_models import (ResearchPosition, Major, ResearchTopic, ProgrammingLanguage, Course)

@bp_faculty.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    form = ResearchPositionForm()

    if form.validate_on_submit():

        
        deadline_value = None
        if form.deadline.data:
            deadline_value = datetime.strptime(form.deadline.data, "%Y-%m-%d")

        # Create position
        position = ResearchPosition(
            title=form.title.data,
            description=form.description.data,
            required_qualifications=form.required_qualifications.data,
            preferred_qualifications=form.preferred_qualifications.data,
            deadline=deadline_value,
            num_positions=form.num_positions.data,
            faculty_id=current_user.id,
        )

        # --- Many-to-Many Selections ---
        # Majors
        if form.majors.data:
            selected_majors = Major.query.filter(Major.id.in_(form.majors.data)).all()
            position.majors.extend(selected_majors)

        # Topics
        if form.topics.data:
            selected_topics = ResearchTopic.query.filter(
                ResearchTopic.id.in_(form.topics.data)
            ).all()
            position.topics.extend(selected_topics)

        # Languages
        if form.languages.data:
            selected_langs = ProgrammingLanguage.query.filter(
                ProgrammingLanguage.id.in_(form.languages.data)
            ).all()
            position.languages.extend(selected_langs)

        # Courses
        if form.courses.data:
            selected_courses = Course.query.filter(
                Course.id.in_(form.courses.data)
            ).all()
            position.courses.extend(selected_courses)

        db.session.add(position)
        db.session.commit()

        flash("Research position created!", "success")
        return redirect(url_for("faculty.view_positions"))

    return render_template("faculty/create_position.html", form=form)




@bp_faculty.route('/position/<int:position_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_position(position_id):

    # Must be a faculty member
    if not current_user.is_faculty:
        abort(403)

    position = ResearchPosition.query.get_or_404(position_id)

    # Only owner faculty can edit
    if position.faculty_id != current_user.id:
        abort(403)

    form = ResearchPositionForm(obj=position)

    if request.method == "GET":
        form.majors.data     = [m.id for m in position.majors]
        form.topics.data     = [t.id for t in position.topics]
        form.languages.data  = [l.id for l in position.languages]
        form.courses.data    = [c.id for c in position.courses]

        # Format date
        if position.deadline:
            form.deadline.data = position.deadline.strftime("%Y-%m-%d")

    if form.validate_on_submit():

        # Update simple fields
        position.title = form.title.data
        position.description = form.description.data
        position.required_qualifications = form.required_qualifications.data
        position.preferred_qualifications = form.preferred_qualifications.data
        position.num_positions = form.num_positions.data

        # Update deadline
        position.deadline = None
        if form.deadline.data:
            position.deadline = datetime.strptime(form.deadline.data, "%Y-%m-%d")

        # Clear and replace many-to-many
        position.majors    = Major.query.filter(Major.id.in_(form.majors.data)).all()
        position.topics    = ResearchTopic.query.filter(ResearchTopic.id.in_(form.topics.data)).all()
        position.languages = ProgrammingLanguage.query.filter(ProgrammingLanguage.id.in_(form.languages.data)).all()
        position.courses   = Course.query.filter(Course.id.in_(form.courses.data)).all()

        db.session.commit()

        flash("Position updated!", "success")
        return redirect(url_for("faculty.view_positions"))

    return render_template("faculty/edit_position.html", form=form, position=position)

@bp_faculty.route('/', methods=['GET'])
@bp_faculty.route('/faculty/index', methods=['GET'])
@login_required
def index():
    all_positions = db.session.scalars(sqla.select(ResearchPosition)).all()
    # all_posts  = positions.all() 
    return render_template('faculty_index.html', title="Research Portal", positions=all_positions)

@bp_faculty.route('/faculty/profile', methods=['GET'])
@login_required
def viewProfile():
    # empty_form = EmptyForm()
    return render_template('display_profile.html', title = "Display Profile", faculty = current_user)
