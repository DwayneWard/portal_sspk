import datetime
import json

from redis import ConnectionPool, StrictRedis

from control_panel.models import ResultTask
from portal.settings import CELERY_BROKER_URL

from .celery import app


@app.task
def check_status_task():
    pool = ConnectionPool.from_url(CELERY_BROKER_URL)
    redis = StrictRedis(connection_pool=pool)

    now = datetime.datetime.now() - datetime.timedelta(days=14)
    result_tasks = ResultTask.objects.filter(datetime__lte=now)

    deleted_result_task = {'result': []}

    if len(result_tasks) != 0:
        for result_task in result_tasks:
            deleted_result_task['result'].append(result_task.delete())

    redis.set(f'check_status_task-{check_status_task.request.id}',
              json.dumps(deleted_result_task, default=str))

    return deleted_result_task
