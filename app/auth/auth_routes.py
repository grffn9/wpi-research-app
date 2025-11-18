
from flask import render_template, flash, redirect, url_for

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla

# @bp_auth.route('/user/login', methods = ['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))

#     lform = LoginForm()

#     #if the lform is validated
#     if lform.validate_on_submit():
#         query = sqla.select(User).where(User.username == lform.username.data)
#         user = db.session.scalars(query).first()
#         if(user is None) or (user.check_password(lform.password.data) == False):
#             #redirect back to login
#             #Invalid username or password
#             flash('Invalid username or password')
#             return redirect(url_for('auth.login'))
        
#         #login user and redirect to index page
#         login_user(user, remember = lform.remember_me.data)
#         flash('the user {} has successfully logged in!'.format(current_user.username))
#         return redirect(url_for('main.index'))
#     return render_template('login.html', form = lform)


# @bp_auth.route('/user/logout', methods = ['GET'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))



