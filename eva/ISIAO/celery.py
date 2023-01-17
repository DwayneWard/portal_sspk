import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('isiao')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_status_task': {
        'task': 'ISIAO.tasks.check_status_task',
        'schedule': crontab(hour=0, minute=0),
    },
}
