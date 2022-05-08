# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.
import logging
import os

import dash
import redis

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_login import login_required
from flask.helpers import get_root_path

from app.settings import DATA_FMT, LOGGING_FILE, LOGGING_FORMAT, Develop, Prod

logging.basicConfig(filename=LOGGING_FILE,
                    filemode='a',
                    format=LOGGING_FORMAT,
                    level=logging.DEBUG,
                    datefmt=DATA_FMT)

# Initialize Flask Application
def populate_cache(app):
    from .models.feedeater_models import Feed

    with app.app_context():
        feeds = Feed.query.all()

    return feeds

def create_app():
    """Creates Flask instance"""
    server = Flask(__name__)
    mode = os.environ.get('MODE') or 'Develop'
    if mode == 'Develop':
        settings_obj = Develop
    else:
        settings_obj = Prod

    server.config.from_object(settings_obj)
    logging.info(f"Starting flask in {mode} mode ...")

    register_extensions(server)
    register_blueprints(server)
    register_dashapps(server)
    register_commands(server)

    return server

def register_extensions(server):
    from app.extensions import celery
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate
    from app.extensions import bootstrap
    from app.extensions import mail
    from app.extensions import csrf_protect

    bootstrap.init_app(server)
    CORS(server)
    with server.app_context():
        db.init_app(server)
        login.init_app(server)
        login.login_view = 'auth_bp.login'
        mail.init_app(server)
        csrf_protect.init_app(server)
        migrate.init_app(server, db)
        celery.init_app(server)

def register_commands(server):
    from app import commands
    server.cli.add_command(commands.init_db)
    server.cli.add_command(commands.create_users)
    server.cli.add_command(commands.create_feeds)


def register_blueprints(server):
    # Import parts of our application TODO : to be separated in several functional parts
    from .views import main_blueprint

    # Register Blueprints
    server.register_blueprint(main_blueprint)


def register_wtforms(server):
     # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    server.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter


def register_UserManagement(server):
    #TODO to be replaced by something else. Check Flask-Security-too package
    from flask_user import UserManager
    # Setup Flask-User to handle user account related forms
    from .models.user_models import User
    from .views.main_views import user_profile_page

    # Setup Flask-User
    user_manager = UserManager(server, db, User)
    
    @server.context_processor
    def context_processor():
        return dict(user_manager=user_manager)


def register_dashapps(app):
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_example = dash.Dash(__name__,
                             server=app,
                             url_base_pathname='/dashboard/',
                             assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                             meta_tags=[meta_viewport])

    with app.app_context():
        from app.dash_example.layout import layout
        from app.dash_example.callbacks import register_callbacks
        dash_example.title = 'Dash quotes'
        dash_example.layout = layout
        register_callbacks(dash_example)

    _protect_dashviews(dash_example)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])


def create_app(extra_config_settings={}):
    """Create a Flask application.
    """
    server = Flask(__name__)
    mode = os.environ.get('MODE') or 'Develop'
    if mode == 'Develop':
        settings_obj = Develop
    else:
        settings_obj = Prod

    # Load settings
    server.config.from_object(settings_obj)
    logging.info(f"Starting flask in {mode} mode ...")
    
    # Load extra settings from extra_config_settings param
    server.config.update(extra_config_settings)

    from app.models.user import User
    
    register_extensions(server)
    register_blueprints(server)
    register_dashapps(server)
    #register_UserManagement(server)
   
    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(server)
    print("create app done")

    return server


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    if app.debug: return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS'] # TODO get admins from user table
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')





