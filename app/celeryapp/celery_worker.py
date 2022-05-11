"""
Run using the command:

python celery -A app.celeryapp.celery_worker.celery worker --concurrency=2 -E -l info
"""
from app import celeryapp, create_app

app = create_app()
celery = celeryapp.celery

