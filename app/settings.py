# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import sys
from os import path, makedirs, environ

from dataclasses import dataclass
from environs import Env

# Env variable config

ENV_FILE = './.env'

if path.exists(ENV_FILE):
    envir = Env()
    envir.read_env()
else:
    print("Error: .env file not found")
    sys.exit(1)

TOKEN = envir('TOKEN')

LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
DATA_FMT = '%y.%b.%d %H:%M:%S'

LOGGING_FILE = "logs/logs.log"

if not path.exists("logs"):
    makedirs("logs")

@dataclass
class Config:
    # Application settings
    APP_NAME = "Flask-Celery-SQLAlchemy"
    APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

    # Flask settings
    CSRF_ENABLED = True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-User settings
    USER_APP_NAME = APP_NAME
    USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
    USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
    USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
    USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
    USER_ENABLE_EMAIL = True  # Register with Email
    USER_ENABLE_REGISTRATION = True  # Allow new users to register
    USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
    USER_ENABLE_USERNAME = False  # Register and Login with username
    USER_AFTER_LOGIN_ENDPOINT = 'main.member_page'
    USER_AFTER_LOGOUT_ENDPOINT = 'main.home_page'
    
    SECRET_KEY = envir("TOKEN")
    REGISTRATION_CLOSED = int(envir("REGISTRATION_CLOSED"))
    DATABASE_FORMAT = envir("DATABASE_FORMAT")
    if DATABASE_FORMAT == 'sqlite':
        DATABASE_STORE = envir("DATABASE_STORE")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_STORE
    elif DATABASE_FORMAT == 'postgresql':
        user = envir("DATABASE_USER")
        password = envir("DATABASE_PASSWORD")
        database = envir("DATABASE_NAME")
        host = envir("DATABASE_HOST")
        port = envir("DATABASE_PORT")
        SQLALCHEMY_DATABASE_URI = (f"postgresql://{user}:{password}@{host}:{port}/{database}")


@dataclass
class Develop(Config):
    """Develop loader"""
    FLASK_ENV = 'development'
    DEBUG = True
    testing = True


@dataclass
class Prod(Config):
    """ Production loader """
    FLASK_ENV = 'production'
    DEBUG = False
    testing = False







TESTING = False

# Celery
CELERY_REDIS_USE_SSL = False
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
