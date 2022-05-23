"""
This resolves the issue of celery and flask instances having access to the same db object
"""
# pylint: disable-all
import flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from app.scheduled_tasks import TASK_SCHEDULE
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_security import Security
from flask_admin import Admin
from authlib.integrations.flask_client import OAuth
import sys

IN_CELERY_WORKER_PROCESS = sys.argv and 'worker' in sys.argv

class FlaskCelery(Celery):
    """Celery class wrapper to make it work with flask instance"""

    def __init__(self, *args, **kwargs):
        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            """Adds flask context to the celery task"""
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.autodiscover_tasks(packages=['app.core.tasks', 'app.rssapp.tasks'])
        self.conf.beat_schedule = TASK_SCHEDULE
        self.config_from_object(app.config)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap5()
csrf_protect = CSRFProtect()
mail = Mail()
security = Security()
admin = Admin()
oauth = OAuth()
