from app.celeryapp import celery
from flask import current_app
from app.extensions import mail
from flask_mail import Message
import logging

@celery.task
def send_flask_mail(**kwargs):
    # If you use Flask_Mail - it needs an app context
    with current_app.app_context():
        mail.send(Message(**kwargs))


@celery.task
def dummy_task(**kwargs):
    logging.info("Dummy task launched")