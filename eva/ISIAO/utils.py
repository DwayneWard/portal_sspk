from redis import ConnectionPool, StrictRedis

from eva.ISIAO.models import GIS, Indicator
from portal.settings import CELERY_BROKER_URL


def get_connect_with_redis():
    """
    Осуществляет к подключение к Redis.
    """
    pool = ConnectionPool.from_url(CELERY_BROKER_URL)
    redis = StrictRedis(connection_pool=pool)
    return redis


def convert_date(date: str = None, format: str = 'month') -> tuple:
    """
    Функция для конвертации даты в формат необходимый для ИС ИАО. Возвращает кортеж из даты в нужном формате и формат.

    :param date: Дата полученная из функции get_date(month=True) в формате строки.
    :param format: Задает необходимый формат для возврата. Возможные значения: month (значение по умолчанию), quarter, half_year и year.
    :return: Возвращает кортеж из даты в нужном формате и формат, если была передана дата. Возвращенный кортеж используется в generate_data.
    """

    dates = {
        'quarters': {
            '01': '-Q4',
            '04': '-Q1',
            '07': '-Q2',
            '10': '-Q3',
        },
        'half_years': {
            '07': '-H1',
            '01': '-H2'
        }
    }

    year, month = date.split('-')
    if format == 'quarter' and date:
        for quarter in dates['quarters']:
            if month == quarter:
                return (year+dates['quarters'][quarter], format)
    if format == 'half_year' and date:
        for half_year in dates['half_years']:
            if month == half_year:
                return (year+dates['half_years'][half_year], format)
    if format == 'year' and date:
        return (year, format)
    return (date, format)


def generate_data(time: str = None, periodic: str = 'day') -> dict:
    """
    Функция для генерации данных для отправки в ИС ИАО. Возвращает словарь.

    :param time: Дата полученная из функции convert_date в формате строки. Это дата за которую отправляются данные, она может быть день/неделя/месяц/квартал/полугодие/год.
    :param periodic: Параматер совпадает с time, но используется для фильтрации показателей, которые необходимо отправить в текущую дату. Возможные значения: day/week/month/quarter/half_year/year.
    :return: Возвращает словарь с данными готовыми для отправки в ИС ИАО.
    """

    data_for_iac = {
        "body": {
            "action": "LOAD_SERIES",
            "datasets": [],
        }
    }

    datasets = []
    codes = Indicator.objects.filter(periodicity=periodic)
    systems = GIS.objects.filter(dashboard_code__isnull=False).filter(zammad_systemcode__isnull=False)
    for code in codes:
        dataset = {
            'indicatorCode': code.ias_code,
            'series': []
        }
        for system in systems:
            # TODO: добавить сюда функцию, которая получает данные из Zammad БД согласно SQL запросу zammad_queryset.
            dataset['series'].append(system.generate_series(value=0, times=time))
        datasets.append(dataset)
    data_for_iac['body']['datasets'] = datasets

    return data_for_iac


def forming_data_by_gis_for_ias():
    pass
