"""
Schedule for tasks that need to be run periodically
"""

from celery.schedules import crontab
import logging

TASK_SCHEDULE = {
    # Runs every minute
    'dummy_task_every_minutes': {
        'task': 'app.core.tasks.dummy_task',
        #'schedule': crontab(minute=0, hour='*/1')
        'schedule': crontab(minute='*')
    },
    # Runs every hours
    'dummy_task_every_hours': {
        'task': 'app.core.tasks.dummy_task',
        'schedule': crontab(minute=0, hour='*/1')
    },
}



