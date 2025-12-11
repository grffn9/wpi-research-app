import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'research.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(basedir, 'app//static')
    TEMPLATE_FOLDER_FACULTY = os.path.join(basedir, 'app//faculty//templates')
    TEMPLATE_FOLDER_STUDENT = os.path.join(basedir, 'app//student//templates')
    TEMPLATE_FOLDER_ERRORS = os.path.join(basedir, 'app//errors//templates')
    TEMPLATE_FOLDER_AUTH = os.path.join(basedir, 'app//auth//templates') 

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    # MAIL_USERNAME = 'researchteampy@gmail.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')

    # MAIL_PASSWORD = os.environ.get('PASSWORD')
    #MAIL_PASSWORD = "lyne xpwd duym oefg" 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI")

    FACULTY_EMAIL_DOMAIN = "@example.com"  

    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False