import datetime
import json

import requests
from redis.exceptions import ConnectionError as DoesNotConnectRedis

from control_panel.models import TaskResult
from eva.isiao.utils import (convert_date, generate_data,
                             get_connect_with_redis, get_name_task_to_db)
from eva.utils import get_date
from portal.settings import IAS_TOKEN, IAS_URL

from .celery import app


@app.task
def check_status_task():
    """
    Автоматическая таска, которая каждый день в полночь будет удалять данные из БД в таблице
    'Результат выполнения отправки данных в ИС ИАО' старше 14 дней и записывать удаленые значения в redis (на время
    тестирования).
    """
    try:
        redis = get_connect_with_redis()

        now = datetime.date.today() - datetime.timedelta(days=14)
        result_tasks = TaskResult.objects.filter(date__lte=now)

        deleted_result_task = {'result': []}

        if len(result_tasks) != 0:
            for result_task in result_tasks:
                deleted_result_task['result'].append(result_task)
                result_task.delete()

        redis.rpush(check_status_task, json.dumps(deleted_result_task, default=str))
    except DoesNotConnectRedis as ex:
        # TODO: 'detail': 'Не могу подключиться к redis. Сообщите администратору системы или в отдел сопровождения СПО'
        pass


@app.task(bind=True, autoretry_for=(SyntaxError, ConnectionError, KeyError), max_retries=5, countdown=30 * 60)
def send_data_to_ias_everyday(self, date: datetime = None):
    """
    Автоматическая таска, которая каждый день в 2 часа ночи будет собирать данные для ИС ИАО согласно требуемой
    периодичности и отправлять их. Записывает результат выполнения в Redis и таблицу в БД
    'Результат выполнения отправки данных в ИС ИАО'. В случае выброса ошибки будет повторять задачу 5 раз с
    периодичностью в 30 минут.
    """
    try:
        redis = get_connect_with_redis()

        if date:
            time = get_date(date=date)
            now = date.strftime('%Y-%m-%d')
        else:
            time = get_date()
            now = datetime.date.today().strftime('%Y-%m-%d')

        data_for_ias = generate_data(*convert_date(time, 'day'))

        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {IAS_TOKEN}',
                   }

        response = requests.post(IAS_URL, headers=headers, data=json.dumps(data_for_ias))
        text = json.loads(response.text)
        if response.status_code == 200:
            redis.set(f'{now}_everyday', json.dumps({'task_id': self.request.id,
                                                     'requestId': text['requestId'],
                                                     'datasets': data_for_ias['body']['datasets']}))
            redis.expire(f'{now}_everyday', 259200)
            result_task, created = TaskResult.objects.update_or_create(
                date=now, periodicity='day', color='green',
                full_name=f'{get_name_task_to_db("day")} выгрузка показателей.', body=data_for_ias['body']['datasets']
            )
        else:
            redis.set(f'{now}_everyday', json.dumps({'task_id': self.request.id,
                                                     'status': response.status_code}))
            redis.expire(f'{now}_everyday', 259200)
            result_task, created = TaskResult.objects.update_or_create(
                date=now, periodicity='day', color='yellow',
                full_name=f'{get_name_task_to_db("day")} выгрузка показателей.', body=data_for_ias['body']['datasets']
            )
    except (SyntaxError, ConnectionError, KeyError) as ex:
        now = datetime.date.today().strftime('%Y-%m-%d')
        result_task, created = TaskResult.objects.update_or_create(
            date=now, periodicity='day', color='red', full_name=f'{get_name_task_to_db("day")} выгрузка показателей.',
            body=ex,
        )
        # TODO: Добавить потом отправку сообщений в телегу, что таска не отработала.
        raise ex
    except DoesNotConnectRedis as ex:
        # TODO: 'detail': 'Не могу подключиться к redis. Сообщите администратору системы или в отдел сопровождения СПО'
        pass


@app.task(bind=True, autoretry_for=(SyntaxError, ConnectionError, KeyError), max_retries=5, countdown=30 * 60)
def send_data_to_ias_everyweek(self, date: datetime = None):
    """
    Автоматическая таска, которая каждый понедельник в 3 часа ночи будет собирать данные для ИС ИАО согласно требуемой
    периодичности и отправлять их. Записывает результат выполнения в Redis и таблицу в БД
    'Результат выполнения отправки данных в ИС ИАО'. В случае выброса ошибки будет повторять задачу 5 раз с
    периодичностью в 30 минут.
    """
    try:
        redis = get_connect_with_redis()

        if date:
            time = get_date(date=date)
            now = date.strftime('%Y-%m-%d')
        else:
            time = get_date()
            now = datetime.date.today().strftime('%Y-%m-%d')

        data_for_ias = generate_data(*convert_date(time, 'week'))

        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {IAS_TOKEN}',
                   }

        response = requests.post(IAS_URL, headers=headers, data=json.dumps(data_for_ias))
        text = json.loads(response.text)
        if response.status_code == 200:
            redis.set(f'{now}_week', json.dumps({'task_id': self.request.id,
                                                 'requestId': text['requestId'],
                                                 'datasets': data_for_ias['body']['datasets']}))
            redis.expire(f'{now}_week', 259200)
            result_task, created = TaskResult.objects.update_or_create(
                date=now, periodicity='week', color='green',
                full_name=f'{get_name_task_to_db("week")} выгрузка показателей.', body=data_for_ias['body']['datasets']
            )
        else:
            redis.set(f'{now}_week', json.dumps({'task_id': self.request.id,
                                                 'status': response.status_code}))
            redis.expire(f'{now}_week', 259200)
            result_task, created = TaskResult.objects.update_or_create(
                date=now, periodicity='week', color='yellow',
                full_name=f'{get_name_task_to_db("week")} выгрузка показателей.', body=data_for_ias['body']['datasets']
            )
    except (SyntaxError, ConnectionError, KeyError) as ex:
        now = datetime.date.today().strftime('%Y-%m-%d')
        result_task, created = TaskResult.objects.update_or_create(
            date=now, periodicity='week', color='red',
            full_name=f'{get_name_task_to_db("week")} выгрузка показателей.', body=ex,
        )
        # TODO: Добавить потом отправку сообщений в телегу, что таска не отработала.
        raise ex
    except DoesNotConnectRedis as ex:
        # TODO: 'detail': 'Не могу подключиться к redis. Сообщите администратору системы или в отдел сопровождения СПО'
        pass


@app.task(bind=True, autoretry_for=(SyntaxError, ConnectionError, KeyError), max_retries=5, countdown=30 * 60)
def send_data_to_ias_periodic(self, date: datetime = None):
    """
    Автоматическая таска, которая каждый первые день месяца будет собирать данные для ИС ИАО согласно требуемой
    периодичности и отправлять их. Записывает результат выполнения в Redis и таблицу в БД
    'Результат выполнения отправки данных в ИС ИАО'. В случае выброса ошибки будет повторять задачу 5 раз с
    периодичностью в 30 минут.
    Таска отрабатывает для периодичностей: месяц, квартал, полугодие и год.
    """
    try:
        redis = get_connect_with_redis()

        if date:
            time = get_date(date=date)
            now = date.strftime('%Y-%m-%d')
        else:
            time = get_date()
            now = datetime.date.today().strftime('%Y-%m-%d')

        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {IAS_TOKEN}',
                   }

        data_month = generate_data(*convert_date(time, 'month'))
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
                    redis.set(f'{now}_{data[1]}', json.dumps({'task_id': self.request.id,
                                                              'requestId': text['requestId'],
                                                              'datasets': data[0]['body']['datasets']}))
                    redis.expire(f'{now}_{data[1]}', 259200)
                    result_task, created = TaskResult.objects.update_or_create(
                        date=now, periodicity=data[1], color='green',
                        full_name=f'{get_name_task_to_db(data[1])} выгрузка показателей.',
                        body=data[0]['body']['datasets']
                    )
                else:
                    redis.set(f'{now}_{data[1]}', json.dumps({'task_id': self.request.id,
                                                              'status': response.status_code}))
                    redis.expire(f'{now}_{data[1]}', 259200)
                    result_task, created = TaskResult.objects.update_or_create(
                        date=now, periodicity=data[1], color='yellow',
                        full_name=f'{get_name_task_to_db(data[1])} выгрузка показателей.',
                        body=data[0]['body']['datasets']
                    )
    except (SyntaxError, ConnectionError, KeyError) as ex:
        # TODO: Добавить потом отправку сообщений в телегу, что таска не отработала.
        now = datetime.date.today()
        periodics = ['month', 'quarter', 'half_year', 'year']
        for periodic in periodics:
            date, format = convert_date(f'{now.year}-{now.month}', periodic)
            if date:
                result_task, created = TaskResult.objects.update_or_create(
                    date=now, periodicity=format, color='red',
                    full_name=f'{get_name_task_to_db(format)} выгрузка показателей.', body=ex,
                )
        raise ex
    except DoesNotConnectRedis as ex:
        # TODO: 'detail': 'Не могу подключиться к redis. Сообщите администратору системы или в отдел сопровождения СПО'
        pass
