
from flask import render_template, flash, redirect, url_for

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla

# @bp_auth.route('/register', methods=['GET', 'POST'])
# def register():
