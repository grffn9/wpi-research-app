from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(db.Model,UserMixin):
    __tablename__='user'
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), index = True, unique = True, nullable=True)
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True)
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    password_hash : sqlo.Mapped[Optional[str]] =sqlo.mapped_column(sqla.String(256))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
    'polymorphic_identity': 'User',
    'polymorphic_on': user_type
    }

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_firstname(self):
        return self.firstname
    
    def get_lastname(self):
        return self.lastname
    
    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

