import sys
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime, timezone
import sqlalchemy as sqla

from app import db

from app.student.student_forms import EditProfileForm, get_courses, get_grades, get_instructors, ApplicationForm
from app.models.models import StudentCourse, ResearchPosition, Application

from app.student import student_blueprint as bp_student

# @bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET'])
@login_required
def index():
    all_positions = db.session.scalars(sqla.select(ResearchPosition)).all()
    
    applied_ids = []
    if current_user.user_type == 'Student':
        applications = db.session.scalars(
            sqla.select(Application).where(Application.student_id == current_user.id)
        ).all()
        applied_ids = [app.position_id for app in applications]

    return render_template('student_index.html', title="Research Application Portal", positions=all_positions, applied_ids=applied_ids)

@bp_student.route('/profile', methods=['GET'])
@login_required
def profile():
    if current_user.user_type != 'Student':
        flash('Access denied. You must be a student to view this page.')
        return redirect(url_for('student.index'))
    
    applications = db.session.scalars(
        sqla.select(Application).where(Application.student_id == current_user.id).order_by(Application.submit_time.desc())
    ).all()

    return render_template('profile.html', applications=applications)

@bp_student.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.user_type != 'Student':
        flash('Access denied. You must be a student to view this page.')
        return redirect(url_for('student.index'))
    
    form = EditProfileForm()
    
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.wpi_id = form.wpi_id.data
        current_user.gpa = form.gpa.data
        
        current_user.majors_of_student = form.majors.data
        current_user.research_topics = form.research_topics.data
        current_user.programming_languages = form.programming_languages.data
        
        # Update coursework
        current_user.coursework.clear()
        for entry in form.coursework.data:
            coursework_entry = StudentCourse(
                course=entry['course'],
                instructor=entry['instructor'],
                grade=entry['grade'],
            )
            current_user.coursework.append(coursework_entry)
        
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('student.profile'))
        
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.wpi_id.data = current_user.wpi_id
        form.gpa.data = current_user.gpa
        
        form.majors.data = current_user.majors_of_student
        form.research_topics.data = current_user.research_topics
        form.programming_languages.data = current_user.programming_languages
        
        for course_record in current_user.coursework:
            form.coursework.append_entry({
                'course': course_record.course,
                'grade': course_record.grade,
                'instructor': course_record.instructor
            })
        
    return render_template('edit_profile.html', title='Edit Profile', form=form,
        course_choices=[(c.id, f"{c.coursenum} - {c.title}") for c in get_courses()],
        grade_choices=[(g.id, g.value) for g in get_grades()],
        instructor_choices=[(i.id, i.name) for i in get_instructors()]
    )

@bp_student.route('/apply/<int:position_id>', methods=['GET', 'POST'])
@login_required
def apply(position_id):
    if current_user.user_type != 'Student':
        flash('Access denied. You must be a student to apply.')
        return redirect(url_for('student.index'))

    position = db.session.get(ResearchPosition, position_id)
    if not position:
        flash('Position not found.')
        return redirect(url_for('student.index'))

    # Check if already applied
    existing_application = db.session.scalars(
        sqla.select(Application).where(
            Application.student_id == current_user.id,
            Application.position_id == position.id
        )
    ).first()

    if existing_application:
        flash('You have already applied to this position.')
        return redirect(url_for('student.index'))

    form = ApplicationForm()
    
    if form.validate_on_submit():
        if position.reference_required and not form.reference.data:
            flash('This position requires a faculty reference.')
            return render_template('apply.html', title='Apply', form=form, position=position)
        
        if not form.statement.data:
            flash('A statement is required.')
            return render_template('apply.html', title='Apply', form=form, position=position)

        application = Application(
            student_id=current_user.id,
            position_id=position.id,
            statement=form.statement.data,
            submit_time = datetime.now(timezone.utc),
            status='pending'
        )
        
        if form.reference.data:
            application.reference_id = form.reference.data.id
            application.reference_status = 'pending'
            
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!')
        return redirect(url_for('student.index'))

    return render_template('apply.html', title='Apply', form=form, position=position)

@bp_student.route('/position/view/<int:position_id>', methods=['GET'])
@login_required
def view_pos(position_id):
    if current_user.user_type != 'Student':
        flash('Access denied. You must be a student to view this position.')
        return redirect(url_for('student.index'))
    position = db.session.scalars(
        sqla.select(ResearchPosition).where(ResearchPosition.id == position_id)).first()
    if not position:
        flash('Position not found.')
        return redirect(url_for('student.index'))
    return render_template('view_pos_details.html', title='View Position', position=position)
