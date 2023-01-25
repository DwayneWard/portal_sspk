import datetime
import json

import requests

from control_panel.models import ResultTask
from eva.isiao.utils import convert_date, generate_data, get_connect_with_redis
from eva.utils import get_date
from portal.settings import IAS_TOKEN, IAS_URL

from .celery import app


@app.task
def check_status_task():
    redis = get_connect_with_redis()

    now = datetime.datetime.now() - datetime.timedelta(days=14)
    result_tasks = ResultTask.objects.filter(datetime__lte=now)

    deleted_result_task = {'result': []}

    if len(result_tasks) != 0:
        for result_task in result_tasks:
            deleted_result_task['result'].append(result_task.delete())

    redis.set(f'check_status_task-{check_status_task.request.id}',
              json.dumps(deleted_result_task, default=str))

    return deleted_result_task


@app.task(bind=True, autoretry_for=(SyntaxError, ConnectionError,), retry_kwargs={'max_retries': 5, 'countdown': 30*60})
def send_data_to_ias_everyday(self):
    try:
        redis = get_connect_with_redis()

        time = get_date()
        now = datetime.datetime.now().strftime('%Y-%m-%d')

        data_for_ias = generate_data(time=time, periodic='day')

        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {IAS_TOKEN}',
                   }

        response = requests.post(IAS_URL, headers=headers, data=json.dumps(data_for_ias))
        text = json.loads(response.text)
        if response.status_code == 200:
            redis.set(f'{now}_everyday',  json.dumps({'task_id': self.request.id,
                                                      'requestId': text['requestId'],
                                                      'datasets': data_for_ias['body']['datasets']}))
            redis.expire(f'{now}_everyday', 259200)
        else:
            redis.set(f'{now}_everyday_code',  json.dumps({'task_id': self.request.id,
                                                           'status': response.status_code}))
            redis.expire(f'{now}_everyday_code', 259200)
    except (SyntaxError, ConnectionError) as ex:
        redis.set(f'{now}_everyday',  json.dumps({'task_id': self.request.id, 'error': repr(ex)}))
        redis.expire(f'{now}_everyday', 259200)
    finally:
        pass


@app.task(bind=True, autoretry_for=(SyntaxError, ConnectionError,), retry_kwargs={'max_retries': 5, 'countdown': 30*60})
def send_data_to_ias_everyweek(self):
    try:
        redis = get_connect_with_redis()

        time = get_date(week=True)
        now = datetime.datetime.now().strftime('%Y-%m-%d')

        data_for_ias = generate_data(time=time, periodic='week')

        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {IAS_TOKEN}',
                   }

        response = requests.post(IAS_URL, headers=headers, data=json.dumps(data_for_ias))
        text = json.loads(response.text)
        if response.status_code == 200:
            redis.set(f'{now}_week',  json.dumps({'task_id': self.request.id,
                                                  'requestId': text['requestId'],
                                                  'datasets': data_for_ias['body']['datasets']}))
            redis.expire(f'{now}_week', 259200)
        else:
            redis.set(f'{now}_week_code',  json.dumps({'task_id': self.request.id,
                                                  'status': response.status_code}))
            redis.expire(f'{now}_week_code', 259200)
    except (SyntaxError, ConnectionError) as ex:
        redis.set(f'{now}_week',  json.dumps({'task_id': self.request.id, 'error': repr(ex)}))
        redis.expire(f'{now}_week', 259200)
    finally:
        pass


@app.task(bind=True, autoretry_for=(SyntaxError, ConnectionError,), retry_kwargs={'max_retries': 5, 'countdown': 30*60})
def send_data_to_ias_periodic(self):
    try:
        redis = get_connect_with_redis()

        time = get_date(month=True)
        now = datetime.datetime.strftime('%Y-%m-%d')

        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {IAS_TOKEN}',
                   }

        data_month = generate_data(*convert_date(time))
        data_quarter = generate_data(*convert_date(time, 'quarter'))
        data_half_year = generate_data(*convert_date(time, 'half_year'))
        data_year = generate_data(*convert_date(time, 'year'))

        datas = [
            (data_month, 'month'),
            (data_quarter, 'quarter'),
            (data_half_year, 'half_year'),
            (data_year, 'year')
        ]
        for data in datas:
            if data[0]['body']['datasets'] != 0:
                response = requests.post(IAS_URL, headers=headers, data=json.dumps(data[0]))
                text = json.loads(response.text)
                if response.status_code == 200:
                    redis.set(f'{now}_{data[1]}',  json.dumps({'task_id': self.request.id,
                                                                'requestId': text['requestId'],
                                                               'datasets': data[0]['body']['datasets']}))
                    redis.expire(f'{now}_{data[1]}', 259200)
                else:
                    redis.set(f'{now}_{data[1]}_code',  json.dumps({'task_id': self.request.id,
                                                                    'status': response.status_code}))
                    redis.expire(f'{now}_{data[1]}_code', 259200)
            else:
                redis.set(f'{now}_{data[1]}',  json.dumps({'task_id': self.request.id,
                                                           'error': data[0]['body']['datasets']}))
                redis.expire(f'{now}_{data[1]}', 259200)
    except (SyntaxError, ConnectionError) as ex:
        redis.set(f'{now}_month/quarter/half_year/year',  json.dumps({'task_id': self.request.id, 'error': repr(ex)}))
        redis.expire(f'{now}_month/quarter/half_year/year', 259200)
    finally:
        pass
