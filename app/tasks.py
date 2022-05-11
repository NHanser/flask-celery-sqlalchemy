from app.celeryapp import celery
from app.services import FeedEater
import logging

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
