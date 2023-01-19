import datetime
import json

import requests

from control_panel.models import ResultTask
from eva.ISIAO.utils import convert_date, generate_data, get_connect_with_redis
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


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 30*60})
def send_data_to_ias_everyday():
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
            redis.set(f'{now}_everyday', {'requestId': text['requestId'], 'datasets': data_for_ias['body']['datasets']})
            redis.expire(f'{now}_everyday', 259200)
        else:
            redis.set(f'{now}_everyday', {'error': text})
            redis.expire(f'{now}_everyday', 259200)
    # TODO: Заменить Exception на конкретную ошибку в ходе тестирования функциональности.
    except Exception as ex:
        redis.set(f'{now}_everyday', {'error': ex})
        redis.expire(f'{now}_everyday', 259200)
    finally:
        pass


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 30*60})
def send_data_to_ias_everyweek():
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
            redis.set(f'{now}_week', {'requestId': text['requestId'], 'datasets': data_for_ias['body']['datasets']})
            redis.expire(f'{now}_week', 259200)
        else:
            redis.set(f'{now}_week', {'error': text})
            redis.expire(f'{now}_week', 259200)
    # TODO: Заменить Exception на конкретную ошибку в ходе тестирования функциональности.
    except Exception as ex:
        redis.set(f'{now}_week', {'error': ex})
        redis.expire(f'{now}_week', 259200)
    finally:
        pass


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 30*60})
def send_data_to_ias_periodic():
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

        if len(data_month['body']['datasets']) != 0 or len(data_quarter['body']['datasets']) != 0 or \
                len(data_half_year['body']['datasets']) != 0 or len(data_year['body']['datasets']) != 0:
            datas = [
                (data_month, 'month'),
                (data_quarter, 'quarter'),
                (data_half_year, 'half_year'),
                (data_year, 'year')
            ]
            for data in datas:
                response = requests.post(IAS_URL, headers=headers, data=json.dumps(data[0]))
                text = json.loads(response.text)
                if response.status_code == 200:
                    redis.set(f'{now}_{data[1]}', {'requestId': text['requestId'],
                                                   'datasets': data[0]['body']['datasets']})
                    redis.expire(f'{now}_{data[1]}', 259200)
                else:
                    redis.set(f'{now}_{data[1]}', {'error': text})
                    redis.expire(f'{now}_{data[1]}', 259200)
    # TODO: Заменить Exception на конкретную ошибку в ходе тестирования функциональности.
    except Exception as ex:
        if len(data_month['body']['datasets']) != 0 or len(data_quarter['body']['datasets']) != 0 or \
                len(data_half_year['body']['datasets']) != 0 or len(data_year['body']['datasets']) != 0:
            redis.set(f'{now}_month/quarter/half_year/year', {'error': ex})
            redis.expire(f'{now}_month/quarter/half_year/year', 259200)
        else:
            redis.set(f'{now}_month', {'error': ex})
            redis.expire(f'{now}_month', 259200)
    finally:
        pass
