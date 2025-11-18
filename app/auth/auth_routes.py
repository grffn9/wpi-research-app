
from flask import render_template, flash, redirect, request, url_for

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla

from flask import current_app, url_for
from flask_login import login_user, current_user, logout_user, login_required

from app.auth.auth_forms import LoginForm, FacultyRegistrationForm
from app.auth.auth_models import User
from app.faculty.faculty_models import Faculty



@bp_auth.route('/register-faculty/<faculty_id>', methods=['GET', 'POST'])
def register_faculty(faculty_id):
    if current_user.is_authenticated:
        return redirect(url_for('faculty.index'))
    
    rform = FacultyRegistrationForm()

    faculty = db.session.get(Faculty, faculty_id)    

    if rform.validate_on_submit():
        faculty.username = rform.username.data
        faculty.set_password(rform.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('faculty_register.html', form = rform)


@bp_auth.route('/user/select-faculty', methods = ['GET'])
def SelectFaculty():
    faculty_list = Faculty.query.all()
    return render_template('select_faculty.html', faculty_list=faculty_list)



@bp_auth.route('/user/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        #choose the correct user
        return redirect(url_for('student.index'))

    lform = LoginForm()

    #if the lform is validated
    if lform.validate_on_submit():
        query = sqla.select(User).where(User.email == lform.email.data)
        user = db.session.scalars(query).first()
        if(user is None) or (user.check_password(lform.password.data) == False):
            #redirect back to login
            #Invalid username or password
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        
        #login user and redirect to index page
        login_user(user, remember = lform.remember_me.data)
        flash('the user {} has successfully logged in!'.format(current_user.username))
        
        #choose the correct user with user_type
        return redirect(url_for('student.index'))
    return render_template('login.html', form = lform)


@bp_auth.route('/user/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    #choose the correct user
    return redirect(url_for('auth.login'))



