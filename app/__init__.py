# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.
import logging
import os

import dash
import redis

from flask import Flask, redirect, url_for, request
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_login import login_required, current_user
from flask.helpers import get_root_path
from flask_security import Security, auth_required
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from app.users.models import User, Role
from app.rssapp.models import Feed, FeedResult, Article
from app import celeryapp
from app.extensions import FlaskCelery, IN_CELERY_WORKER_PROCESS
from app.core.forms import ExtendedLoginForm
from app.oauth import oauth_registration
from app.settings import DATA_FMT, LOGGING_FILE, LOGGING_FORMAT, Develop, Prod


logging.basicConfig(#filename=LOGGING_FILE,
                    #filemode='a',
                    format=LOGGING_FORMAT,
                    level=logging.DEBUG,
                    datefmt=DATA_FMT)

from flask_security import RegisterForm, LoginForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ControllerModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('security.login', next=request.endpoint))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')# This does the trick rendering the view only if the user is authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('security.login', next=request.endpoint))

def register_extensions(server):
    from app.extensions import db, login, migrate, bootstrap, mail, csrf_protect, admin, oauth
    from app.extensions import security
    celeryapp.celery = FlaskCelery(app=server)
    with server.app_context():
        bootstrap.init_app(server)
        CORS(server)
        db.init_app(server)
        login.init_app(server)
        mail.init_app(server)
        csrf_protect.init_app(server)
        migrate.init_app(server, db)
        oauth.init_app(server)
        oauth_registration(oauth)
        CSRFProtect(server)
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        from app.core.models import MyMailUtil
        security.init_app(server,
                            user_datastore, 
                            confirm_register_form=RegisterForm,
                            login_form=ExtendedLoginForm,
                            mail_util_cls=MyMailUtil)
        admin.init_app(server, index_view = MyAdminIndexView())
        admin.add_view(ControllerModelView(User, db.session))
        admin.add_view(ControllerModelView(Role, db.session))
        admin.add_view(ControllerModelView(Feed, db.session))
        admin.add_view(ControllerModelView(FeedResult, db.session))
        admin.add_view(ControllerModelView(Article, db.session))



def register_blueprints(server):
    # Import parts of our application TODO : to be separated in several functional parts
    from app.core.routes import core_bp
    from app.oauth import google_blueprint
    from app.commands import commands_bp
    from app.dashapp.routes import dash_bp
    from app.users.routes import users_bp

    # Register Blueprints
    server.register_blueprint(core_bp)
    server.register_blueprint(google_blueprint, url_prefix="/google")
    server.register_blueprint(commands_bp)
    server.register_blueprint(dash_bp)
    server.register_blueprint(users_bp, url_prefix="/user")


def register_wtforms(server):
     # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    server.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter



def register_dashapps(app):
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                             server=app,
                             url_base_pathname='/dashapp/',
                             assets_folder=get_root_path(__name__) + '/dashboard/assets/')

    with app.app_context():
        from app.dashapp.layout import layout
        from app.dashapp.callbacks import register_callbacks
        dashapp.title = 'Dash quotes'
        dashapp.layout = layout
        register_callbacks(dashapp)

    _protect_dashviews(dashapp)


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

    register_extensions(server)
    register_blueprints(server)
    register_dashapps(server)
   
    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(server)

    return server
    

def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    mode = os.environ.get('MODE') or 'Develop'
    if app.debug and mode == "Develop": return  # Do not send error emails while developing

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





