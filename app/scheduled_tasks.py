"""
Schedule for tasks that need to be run periodically
"""

from celery.schedules import crontab
import logging

TASK_SCHEDULE = {
    # Runs every hour
    'dummy_task_every_hours': {
        'task': 'tasks.dummy_task',
        'schedule': crontab(minute=0, hour='*/1')
    },
}



