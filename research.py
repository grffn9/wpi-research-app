from config import Config
from app.auth.auth_models import User
from app.faculty.faculty_models import Faculty
from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'user': User, 'faculty': Faculty}


@sqla.event.listens_for(Faculty.__table__, 'after_create')
def add_faculty(*args, **kwargs):
    query = sqla.select(Faculty)
    if db.session.scalars(query).first() is None:
        faculty_members = [{'firstname':'John','lastname':'Doe','email':'john.doe@example.com', 'is_verified': False},
          {'firstname':'Jane','lastname':'Smith','email':'jane.smith@example.com', 'is_verified': False},
          {'firstname':'Jim','lastname':'Brown','email':'jim.brown@example.com', 'is_verified': False},
          {'firstname':'Harry','lastname':'Davis','email':'harry.davis@example.com', 'is_verified': False}, 
          {'firstname':'Lisa','lastname':'Wilson','email':'lisa.wilson@example.com', 'is_verified': False}  ]
        for m in faculty_members:
            db.session.add(Faculty(firstname = m['firstname'], lastname = m['lastname'], email = m['email'], is_verified = m['is_verified']))
        db.session.commit()


@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)