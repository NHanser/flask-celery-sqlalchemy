# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import sys
from os import path, makedirs, environ

from dataclasses import dataclass
from environs import Env
from flask_security import uia_email_mapper, uia_username_mapper

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

    app_run_env = "LOCAL"
    if "APP_RUN_ENV" in environ:
        app_run_env = environ["APP_RUN_ENV"]

    # Flask settings
    CSRF_ENABLED = True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_REDIS_USE_SSL = envir("CELERY_REDIS_USE_SSL")

    # Need to be able to route backend flask API calls. Use 'accounts'
    # to be the Flask-Security endpoints.
    SECURITY_URL_PREFIX = '/api/accounts'
    SECURITY_PASSWORD_SALT = envir("SECURITY_PASSWORD_SALT")
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_REGISTERABLE = True
    #SECURITY_UNIFIED_SIGNIN = True
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {"email": {"mapper": uia_email_mapper, "case_insensitive": True}},
        {"username": {"mapper": uia_username_mapper, "case_insensitive": True}},
        ]

    # These need to be defined to handle redirects
    # As defined in the API documentation - they will receive the relevant context
    SECURITY_POST_CONFIRM_VIEW = "/confirmed"
    SECURITY_CONFIRM_ERROR_VIEW = "/confirm-error"
    SECURITY_RESET_VIEW = "/reset-password"
    SECURITY_RESET_ERROR_VIEW = "/reset-password"
    SECURITY_REDIRECT_BEHAVIOR = "spa"

    # CSRF protection is critical for all session-based browser UIs

    # enforce CSRF protection for session / browser - but allow token-based
    # API calls to go through
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # Send Cookie with csrf-token. This is the default for Axios and Angular.
    SECURITY_CSRF_COOKIE_NAME = "XSRF-TOKEN"
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None
    
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

    # Celery
    if app_run_env == "LOCAL":
        CELERY_BROKER_URL = envir("CELERY_BROKER_URL")
        CELERY_BACKEND_URL = envir("CELERY_BACKEND_URL")
    elif app_run_env == "DOCKER":
        CELERY_BROKER_URL = "pyamqp://admin:mypass@myapp-rabbitmq//"
        CELERY_BACKEND_URL = "redis://myapp-redis"
    elif app_run_env == "HEROKU":
        CELERY_BROKER_URL = envir["CLOUDAMQP_URL"]
        CELERY_BACKEND_URL = envir["REDIS_URL"]
    


@dataclass
class Develop(Config):
    """Develop loader"""
    FLASK_ENV = 'development'
    DEBUG = True
    testing = True
    #SECURITY_REDIRECT_HOST = 'localhost:8888'


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
