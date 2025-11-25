# /faculty/profile
import sys
from xml.parsers.expat import model
from flask import render_template, flash, redirect, url_for, abort, request
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

import sqlalchemy as sqla
import sqlalchemy as sqla
from datetime import datetime
from app.faculty.faculty_forms import ResearchPositionForm, AddItemForm
from app import db
from app.faculty import faculty_blueprint as bp_faculty
# from app.faculty.faculty_models import Major, ResearchTopic, ProgrammingLanguage, Course
from app.models.models import Major, ResearchTopic, ProgrammingLanguage, Course

from app.models import Student, ResearchPosition, Application


@bp_faculty.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    form = ResearchPositionForm()
        
    form.preferred_majors.choices = [
        (m.id, m.name) for m in Major.query.order_by(Major.name)]

    form.research_topics.choices = [
        (t.id, t.name) for t in ResearchTopic.query.order_by(ResearchTopic.name)]
       
    form.programming_languages.choices = [
        (l.id, l.name) for l in ProgrammingLanguage.query.order_by(ProgrammingLanguage.name)]
        
    form.required_courses.choices = [
        (c.id, f"{c.coursenum} — {c.title}") for c in Course.query.order_by(Course.coursenum)]
    
    if form.validate_on_submit():

        # Create position
        position = ResearchPosition(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            team_size=form.team_size.data,
            min_gpa=form.min_gpa.data,
            reference_required=form.reference_required.data,
        )

        # --- Many-to-Many Selections ---
        # Majors
        if form.preferred_majors.data:
            major_ids = [m.id for m in form.preferred_majors.data]
            selected_majors = Major.query.filter(Major.id.in_(major_ids)).all()
            position.preferred_majors.extend(selected_majors)

        # Topics
        if form.research_topics.data:
            topic_ids = [t.id if hasattr(t, "id") else int(t) for t in form.research_topics.data]
            selected_topics = ResearchTopic.query.filter(
            ResearchTopic.id.in_(topic_ids)).all()
            position.research_topics.extend(selected_topics)

        # Languages
        if form.programming_languages.data:
            lang_ids = [l.id if hasattr(l, "id") else int(l) for l in form.programming_languages.data]
            selected_langs = ProgrammingLanguage.query.filter(
            ProgrammingLanguage.id.in_(lang_ids)).all()
            position.programming_languages.extend(selected_langs)
        
        # Courses
        if form.required_courses.data:
            course_ids = [c.id if hasattr(c, "id") else int(c) for c in form.required_courses.data]
            selected_courses = Course.query.filter(
            Course.id.in_(course_ids)).all()
            position.required_courses.extend(selected_courses)

        #This is why there was an error with posting positions
        position.faculty = current_user

        db.session.add(position)
        db.session.commit()

        flash("Research position created!", "success")
        return redirect(url_for("faculty.viewProfile"))

    return render_template("create_research_project.html", form=form)




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


    form.preferred_majors.choices = [
        (m.id, m.name) for m in Major.query.order_by(Major.name)]

    form.research_topics.choices = [
        (t.id, t.name) for t in ResearchTopic.query.order_by(ResearchTopic.name)]
       
    form.programming_languages.choices = [
        (l.id, l.name) for l in ProgrammingLanguage.query.order_by(ProgrammingLanguage.name)]
        
    form.required_courses.choices = [
        (c.id, f"{c.coursenum} — {c.title}") for c in Course.query.order_by(Course.coursenum)]

    if request.method == "GET":
        form.majors.data     = [m.id for m in position.majors]
        form.topics.data     = [t.id for t in position.topics]
        form.languages.data  = [l.id for l in position.languages]
        form.courses.data    = [c.id for c in position.courses]

        # Format date
        if position.end_date:
            form.end_date.data = position.end_date.strftime("%Y-%m-%d")

    if form.validate_on_submit():

        # Update simple fields
        position.title = form.title.data
        position.description = form.description.data
        position.required_qualifications = form.required_qualifications.data
        position.preferred_qualifications = form.preferred_qualifications.data
        position.num_positions = form.num_positions.data

        # Update deadline
        position.end_date = None
        if form.end_date.data:
            position.end_date = datetime.strptime(form.end_date.data, "%Y-%m-%d")

        # Clear and replace many-to-many
        position.majors    = Major.query.filter(Major.id.in_(form.majors.data)).all()
        position.topics    = ResearchTopic.query.filter(ResearchTopic.id.in_(form.topics.data)).all()
        position.languages = ProgrammingLanguage.query.filter(ProgrammingLanguage.id.in_(form.languages.data)).all()
        position.courses   = Course.query.filter(Course.id.in_(form.courses.data)).all()

        db.session.commit()

        flash("Position updated!", "success")
        return redirect(url_for("faculty.viewProfile"))

    return render_template("faculty/edit_position.html", form=form, position=position)


@bp_faculty.route('/faculty/index', methods=['GET'])
@login_required
def index():
    all_positions = db.session.scalars(sqla.select(ResearchPosition).where(ResearchPosition.faculty_id == current_user.id)).all()
    # all_posts  = positions.all() 
    return render_template('faculty_index.html', title="Research Portal", positions=all_positions)

@bp_faculty.route('/faculty/profile', methods=['GET'])
@login_required
def viewProfile():
    # empty_form = EmptyForm()
    return render_template('display_profile.html', title = "Display Profile", faculty = current_user)


@bp_faculty.route('/position/<int:position_id>/applicants', methods=['GET', 'POST'])
@login_required
def view_applicants(position_id):

    all_applications = db.session.scalars(sqla.select(Application).where(Application.position_id == position_id)).all()
    return render_template('view_applicants.html', applications=all_applications)


@bp_faculty.route('/position/<int:applicant_id>/', methods=['GET', 'POST'])
@login_required
def view_one_applicant(applicant_id):

    student = db.session.scalars(sqla.select(Student).where(Student.id == applicant_id)).first()
    return render_template('view_one_applicant.html', student=student)

    
