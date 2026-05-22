# /faculty/profile
import sys
from xml.parsers.expat import model
from flask import render_template, flash, redirect, url_for, abort, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required

import sqlalchemy as sqla
from datetime import datetime, timezone
from app.faculty.faculty_forms import ResearchPositionForm,MajorForm, ResearchTopicForm, ProgrammingLanguageForm, CourseForm, RecommendationForm
from app import db
from app.faculty import faculty_blueprint as bp_faculty
# from app.faculty.faculty_models import Major, ResearchTopic, ProgrammingLanguage, Course
from app.models.models import Major, ResearchTopic, ProgrammingLanguage, Course, Faculty
from app.models import Student, ResearchPosition, Application


@bp_faculty.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():

    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    form = ResearchPositionForm()
        
    form.preferred_majors.choices = [
        (m.id, m.name) for m in Major.query.order_by(Major.name)]

    form.research_topics.choices = [
        (t.id, t.name) for t in ResearchTopic.query.order_by(ResearchTopic.name)]
       
    form.programming_languages.choices = [
        (l.id, l.name) for l in ProgrammingLanguage.query.order_by(ProgrammingLanguage.name)]
        
    form.required_courses.choices = [
        (c.id, f"{c.coursenum} — {c.title}") for c in Course.query.order_by(Course.coursenum)]
    
    if form.start_date.data and form.end_date.data:
            if form.end_date.data < form.start_date.data:
                flash("End date cannot be earlier than the start date.", "danger")
                return render_template("create_research_project.html", form=form, faculty=current_user)
            
    if form.team_size.data is not None and form.team_size.data < 1:
        flash("Team size must be at least 1.", "danger")
        return render_template("create_research_project.html", form=form, faculty=current_user)
    
    if form.min_gpa.data is not None:
        if form.min_gpa.data < 0 or form.min_gpa.data > 4.0:
            flash("Minimum GPA must be between 0.0 and 4.0.", "danger")
            return render_template("create_research_project.html", form=form, faculty=current_user)


    
    if form.validate_on_submit():
        

        from datetime import date

        today = date.today()

        if form.start_date.data < today:
            flash("Start date cannot be earlier than today's date.", "danger")
            return render_template("create_research_project.html", form=form, faculty=current_user)

        
        
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
        return redirect(url_for("faculty.index"))

    return render_template("create_research_project.html", form=form, faculty = current_user)




@bp_faculty.route('/position/<int:position_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_position(position_id):

    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
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
        form.preferred_majors.data     = [m.id for m in position.preferred_majors]
        form.research_topics.data     = [t.id for t in position.research_topics]
        form.programming_languages.data  = [l.id for l in position.programming_languages]
        form.required_courses.data    = [c.id for c in position.required_courses]

        # Format date
        if position.end_date:
            form.end_date.data = position.end_date

    if form.start_date.data and form.end_date.data:
            if form.end_date.data < form.start_date.data:
                flash("End date cannot be earlier than the start date.", "danger")
                return render_template("edit_position.html", form=form, position=position, faculty=current_user)
    
    if form.team_size.data is not None and form.team_size.data < 1:
        flash("Team size must be at least 1.", "danger")
        return render_template("edit_position.html", form=form, position=position, faculty=current_user)
    
    if form.min_gpa.data is not None:
        if form.min_gpa.data < 0 or form.min_gpa.data > 4.0:
            flash("Minimum GPA must be between 0.0 and 4.0.", "danger")
            return render_template("edit_position.html", form=form, position=position, faculty=current_user)

    if form.validate_on_submit():

        from datetime import date

        today = date.today()

        if form.start_date.data < today:
            flash("Start date cannot be earlier than today's date.", "danger")
            return render_template("edit_position.html", form=form, position=position, faculty=current_user)

        # Update simple fields
        position.title = form.title.data
        position.description = form.description.data
        position.start_date = form.start_date.data
        position.end_date = form.end_date.data
        position.team_size = form.team_size.data
        position.min_gpa = form.min_gpa.data
        position.reference_required = form.reference_required.data

        # Update many-to-many relationships
        if form.preferred_majors.data:
            major_ids = [m.id if hasattr(m, "id") else int(m) for m in form.preferred_majors.data]
            position.preferred_majors = Major.query.filter(Major.id.in_(major_ids)).all()
        
        if form.research_topics.data:
            topic_ids = [t.id if hasattr(t, "id") else int(t) for t in form.research_topics.data]
            position.research_topics = ResearchTopic.query.filter(ResearchTopic.id.in_(topic_ids)).all()
        
        if form.programming_languages.data:
            lang_ids = [l.id if hasattr(l, "id") else int(l) for l in form.programming_languages.data]
            position.programming_languages = ProgrammingLanguage.query.filter(ProgrammingLanguage.id.in_(lang_ids)).all()
        
        if form.required_courses.data:
            course_ids = [c.id if hasattr(c, "id") else int(c) for c in form.required_courses.data]
            position.required_courses = Course.query.filter(Course.id.in_(course_ids)).all()

        db.session.commit()

        flash("Position updated!", "success")
        return redirect(url_for("faculty.index"))

    return render_template("edit_position.html", form=form, position=position, faculty = current_user)


@bp_faculty.route('/faculty/index', methods=['GET'])
@login_required
def index():

    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    
    all_positions = db.session.scalars(sqla.select(ResearchPosition).where(ResearchPosition.faculty_id == current_user.id)).all()
    # all_posts  = positions.all() 
    return render_template('faculty_index.html', title="Research Portal", positions=all_positions, faculty = current_user)

@bp_faculty.route('/faculty/profile', methods=['GET', 'POST'])
@login_required
def viewProfile():
    
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    # empty_form = EmptyForm()
    if current_user.user_type == 'Faculty':
        current_user.last_notif_time = datetime.now(timezone.utc)
        db.session.commit()
    refs = db.session.scalars(sqla.select(Application).where(Application.reference_id == current_user.id)).all()
    form = RecommendationForm()
    return render_template('display_profile.html', title = "Display Profile", faculty = current_user, referals = refs, form = form)

@bp_faculty.route('/faculty/<int:rec_id>/recommend', methods=['GET', 'POST'])
@login_required
def change_rec_status(rec_id):
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)
    refs = db.session.scalars(sqla.select(Application).where(Application.reference_id == current_user.id)).all()
    form = RecommendationForm()
    if form.validate_on_submit():
        print(rec_id)
        application = db.session.scalars(sqla.select(Application).where(Application.id == rec_id)).first()
        application.reference_status = form.rec_status.data
        db.session.commit()
    return render_template('display_profile.html', title = "Display Profile", faculty = current_user, referals = refs, form = form)

# ------------------ Applicants ------------------
@bp_faculty.route('/position/<int:position_id>/applicants', methods=['GET', 'POST'])
@login_required
def view_applicants(position_id):
    
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    position = db.session.get(ResearchPosition, position_id)
    all_applications = db.session.scalars(sqla.select(Application).where(Application.position_id == position_id)).all()
    return render_template('view_applicants.html', applications=all_applications, faculty = current_user, position=position)


@bp_faculty.route('/position/<int:applicantion_id>/', methods=['GET', 'POST'])
@login_required
def view_one_applicantion(applicantion_id):
    
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    application = db.session.scalars(sqla.select(Application).where(Application.id == applicantion_id)).first()
    student = db.session.scalars(sqla.select(Student).where(Student.id == application.student_id)).first()

    return render_template('view_one_applicantion.html', student=student, application=application, faculty = current_user)



@bp_faculty.route('/application/<int:app_id>/update', methods=['POST'])
@login_required
def update_application_status(app_id):

    
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    app = Application.query.get_or_404(app_id)
    action = request.form.get("action")

    position = app.position  # The research position they applied to

    if action == "accept":
        # ----- Enforce Max Team Size -----
        accepted_count = Application.query.filter_by(
            position_id=position.id,
            status="Accepted"
        ).count()

        if accepted_count >= position.team_size:
            flash("You cannot accept this student — team size limit reached.", "warning")
            return redirect(url_for('faculty.view_one_applicantion', applicantion_id=app.id))

        app.status = "Accepted"
        flash("Application accepted")

    elif action == "reject":
        app.status = "Rejected"
        flash("Application rejected")

    db.session.commit()
    return redirect(url_for('faculty.view_applicants', position_id=position.id, faculty = current_user))



# ------------------ Majors ------------------
@bp_faculty.route('/faculty/majors')
@login_required
def list_majors():
    
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)


    majors = db.session.scalars(sqla.select(Major).order_by(Major.name)).all()
    return render_template('majors_list.html', majors=majors, faculty = current_user)


@bp_faculty.route('/faculty/majors/create', methods=['GET','POST'])
@login_required
def create_major():
    # Must be a faculty member
    if not current_user.user_type == 'Faculty':
        abort(403)

    form = MajorForm()
    if form.validate_on_submit():
        major = Major(
            name=form.name.data,
            department=form.department.data
        )
        db.session.add(major)
        db.session.commit()
        flash('Major created.', 'success')
        return redirect(url_for('faculty.list_majors'))
    return render_template('majors_form.html', form=form, action='Create', faculty = current_user)


@bp_faculty.route('/faculty/majors/<int:major_id>/edit', methods=['GET','POST'])
@login_required
def edit_major(major_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    major = db.session.get(Major, major_id) or abort(404)
    form = MajorForm(obj=major)
    if form.validate_on_submit():
        major.name = form.name.data
        major.department = form.department.data
        db.session.commit()
        flash('Major updated.', 'success')
        return redirect(url_for('faculty.list_majors'))
    return render_template('majors_form.html', form=form, action='Edit', faculty = current_user)


@bp_faculty.route('/faculty/majors/<int:major_id>/delete', methods=['POST'])
@login_required
def delete_major(major_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    major = db.session.get(Major, major_id) or abort(404)
    db.session.delete(major)
    db.session.commit()
    flash('Major deleted.', 'success')
    return redirect(url_for('faculty.list_majors'))



# ------------------ Research Topics ------------------
@bp_faculty.route('/faculty/topics')
@login_required
def list_topics():
    if not current_user.user_type == 'Faculty':
        abort(403)
    topics = db.session.scalars(
        sqla.select(ResearchTopic).order_by(ResearchTopic.name)
    ).all()
    return render_template('topics_list.html', topics=topics, faculty = current_user)

@bp_faculty.route('/faculty/topics/create', methods=['GET','POST'])
@login_required
def create_topic():
    if current_user.user_type != "Faculty":
        abort(403)
    form = ResearchTopicForm()
    if form.validate_on_submit():
        topic = ResearchTopic(
            name=form.name.data,
        )
        db.session.add(topic)
        db.session.commit()
        flash('Research topic created.', 'success')
        return redirect(url_for('faculty.list_topics'))
    return render_template('topics_form.html', form=form, action='Create', faculty = current_user)


@bp_faculty.route('/faculty/topics/<int:topic_id>/edit', methods=['GET','POST'])
@login_required
def edit_topic(topic_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    topic = db.session.get(ResearchTopic, topic_id) or abort(404)
    form = ResearchTopicForm(obj=topic)
    if form.validate_on_submit():
        topic.name = form.name.data
        db.session.commit()
        flash('Research topic updated.', 'success')
        return redirect(url_for('faculty.list_topics'))
    return render_template('topics_form.html', form=form, action='Edit', faculty = current_user)


@bp_faculty.route('/faculty/topics/<int:topic_id>/delete', methods=['POST'])
@login_required
def delete_topic(topic_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    topic = db.session.get(ResearchTopic, topic_id) or abort(404)
    db.session.delete(topic)
    db.session.commit()
    flash('Research topic deleted.', 'success')
    return redirect(url_for('faculty.list_topics'))

# ------------------ Courses ------------------
@bp_faculty.route('/faculty/courses')
@login_required
def list_courses():
    if not current_user.user_type == 'Faculty':
        abort(403)
    Courses = db.session.scalars(sqla.select(Course).order_by(Course.coursenum)).all()
    return render_template('courses_list.html', courses=Courses,  faculty = current_user)


@bp_faculty.route('/faculty/courses/create', methods=['GET','POST'])
@login_required
def create_course():
    if not current_user.user_type == 'Faculty':
        abort(403)
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(coursenum=form.coursenum.data, title=form.title.data, major=form.majorid.data)
        db.session.add(course)
        db.session.commit()
        flash('Course created.', 'success')
        return redirect(url_for('faculty.list_courses'))
    return render_template('courses_form.html', form=form, action='Create',  faculty = current_user)

@bp_faculty.route('/faculty/courses/<int:course_id>/edit', methods=['GET','POST'])
@login_required
def edit_course(course_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    course = db.session.get(Course, course_id) or abort(404)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.coursenum = form.coursenum.data
        course.title = form.title.data
        course.major = form.majorid.data
        db.session.commit()
        flash('Course updated.', 'success')
        return redirect(url_for('faculty.list_courses'))
    return render_template('courses_form.html', form=form, action='Edit', faculty = current_user)

@bp_faculty.route('/faculty/courses/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    course = db.session.get(Course, course_id) or abort(404)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted.', 'success')
    return redirect(url_for('faculty.list_courses'))

#------------------ Languages ------------------
@bp_faculty.route('/faculty/languages')
@login_required
def list_languages():
    if not current_user.user_type == 'Faculty':
        abort(403)
    languages = db.session.scalars(
        sqla.select(ProgrammingLanguage).order_by(ProgrammingLanguage.name)
    ).all()
    return render_template('languages_list.html', languages=languages,  faculty = current_user)


@bp_faculty.route('/faculty/languages/create', methods=['GET','POST'])
@login_required
def create_language():
    if not current_user.user_type == 'Faculty':
        abort(403)
    form = ProgrammingLanguageForm()
    if form.validate_on_submit():
        language = ProgrammingLanguage(
            name=form.name.data,        
        )
        db.session.add(language)
        db.session.commit()
        flash('Programming language created.', 'success')
        return redirect(url_for('faculty.list_languages'))
    return render_template('languages_form.html', form=form, action='Create',  faculty = current_user)


@bp_faculty.route('/faculty/languages/<int:language_id>/edit', methods=['GET','POST'])
@login_required
def edit_language(language_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    language = db.session.get(ProgrammingLanguage, language_id) or abort(404)
    form = ProgrammingLanguageForm(obj=language)
    if form.validate_on_submit():
        language.name = form.name.data
        db.session.commit()
        flash('Programming language updated.', 'success')
        return redirect(url_for('faculty.list_languages'))
    return render_template('languages_form.html', form=form, action='Edit', faculty = current_user)


@bp_faculty.route('/faculty/languages/<int:language_id>/delete', methods=['POST'])
@login_required
def delete_language(language_id):
    if not current_user.user_type == 'Faculty':
        abort(403)
    language = db.session.get(ProgrammingLanguage, language_id) or abort(404)
    db.session.delete(language)
    db.session.commit()
    flash('Programming language deleted.', 'success')
    return redirect(url_for('faculty.list_languages'))

@bp_faculty.route('/faculty/admin')
@login_required
def admin_home():
    if not current_user.user_type == 'Faculty':
        abort(403)
    return render_template('faculty_admin.html', faculty = current_user)

