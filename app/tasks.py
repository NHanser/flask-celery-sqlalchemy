from app.celeryapp import celery
from app.services import FeedEater
import logging
from flask_mail import Mail, Message
from app.extensions import mail
from flask import current_app

logger = logging.getLogger(__name__)

@celery.task(name="fetch_articles_task")
def fetch_articles(feed_id: int):
    logger.info("Fetch articles started")
    feedeater = FeedEater()
    feedeater.fetch(feed_id)


@celery.task(name="dummy_task")
def dummy_task():
    """
    Dummy task
    """
    logger.info("Dummy task started")


@celery.task
def send_flask_mail(**kwargs):
    # If you use Flask_Mail - it needs an app context
    with current_app.app_context():
        mail.send(Message(**kwargs))
