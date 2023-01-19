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
    'send_request_everyday': {
        'task': 'ISIAO.tasks.send_data_to_ias_everyday',
        'schedule': crontab(hour=2, minute=0),
    },
    'send_request_everyweek': {
        'task': 'ISIAO.tasks.send_data_to_ias_everyweek',
        'schedule': crontab(hour=3, minute=0, day_of_week='monday'),
    },
    'send_request_periodic': {
        'task': 'ISIAO.tasks.send_data_to_ias_periodic',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
}