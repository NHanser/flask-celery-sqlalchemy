from app.extensions import celery
from app.services import FeedEater

@celery.task(name="fetch_articles_task")
def fetch_articles(feed_id: int):
    feedeater = FeedEater()
    feedeater.fetch(feed_id)


@celery.task(name="dummy_task")
def dummy_task():
    """
    Dummy task
    """
    logging.info("Dummy task started")
