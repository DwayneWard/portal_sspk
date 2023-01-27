from redis import ConnectionPool, StrictRedis

from eva.isiao.models import GIS, Indicator
from eva.utils import get_cursor_from_zammad_db, get_date
from portal.settings import (CELERY_BROKER_URL, ZAMMAD_DB_HOST, ZAMMAD_DB_NAME,
                             ZAMMAD_DB_PASSWORD, ZAMMAD_DB_PORT,
                             ZAMMAD_DB_USER)


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
    :param format: Задает необходимый формат для возврата. Возможные значения: month (значение по умолчанию), quarter,
    half_year и year.
    :return: Возвращает кортеж из даты в нужном формате и формат, если была, если дата соотвествовала формату, иначе
    (None, format).
    Возвращенный кортеж используется в generate_data.
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
        },
        'year': '01'
    }

    year, month = date.split('-')
    if format == 'quarter' and date:
        for quarter in dates['quarters']:
            if month == quarter:
                return (year + dates['quarters'][quarter], format)
    if format == 'half_year' and date:
        for half_year in dates['half_years']:
            if month == half_year:
                return (year + dates['half_years'][half_year], format)
    if format == 'year' and date:
        if month == dates['year']:
            return (year, format)
    if format == 'month' and date:
        return (f'{year}-{month}', format)
    return (None, format)


def forming_data_by_gis_for_iac(zammad_systemcode, date, indicator: Indicator):
    """
    Получает данные по требуемому ГИСу на основе Показателя ИС ИАО.

    :param zammad_systemcode: Код системы в БД Zammad, который берется из ГИСА -> поле zammad_systemcode.
    :param date: Получаем время в формате строки из функции get_date за вчерашний день.
    :param indicator: Показатель ИС ИАО с соотвествующей периодичностью
    :return: В случае успешного выполнения - данные из БД Zammad, в случае SyntaxError/ConnectionError:
    Сообщение об ошибке.
    """
    zammad_queryset = indicator.zammad_queryset.replace('###system_id###', str(zammad_systemcode)).replace('###date###',
                                                                                                           str(date))
    try:
        cursor = get_cursor_from_zammad_db(
            db=ZAMMAD_DB_NAME,
            host=ZAMMAD_DB_HOST,
            port=ZAMMAD_DB_PORT,
            user=ZAMMAD_DB_USER,
            password=ZAMMAD_DB_PASSWORD,
            queryset=zammad_queryset,
        )
        data = cursor.fetchall()
        return data[0][0]
    except SyntaxError:
        raise SyntaxError('При формировании данных возникла ошибка в SQL-запросе.')
    except ConnectionError:
        raise ConnectionError('При подключении к БД Zammad возникла ошибка.')


def generate_data(time: str = None, periodic: str = 'day') -> dict:
    """
    Функция для генерации данных для отправки в ИС ИАО. Возвращает словарь.


    :param time: Дата полученная из функции convert_date в формате строки. Это дата за которую отправляются данные,
    она может быть день/неделя/месяц/квартал/полугодие/год.
    :param periodic: Параматер совпадает с time, но используется для фильтрации показателей,
    которые необходимо отправить в текущую дату. Возможные значения: day/week/month/quarter/half_year/year.
    :return: Возвращает словарь с данными готовыми для отправки в ИС ИАО, в случае SyntaxError/ConnectionError: raise
    """

    try:
        data_for_iac = {
            "body": {
                "action": "LOAD_SERIES",
                "datasets": [],
            }
        }

        if time:
            datasets = []
            indicators = Indicator.objects.filter(periodicity=periodic)
            systems = GIS.objects.filter(dashboard_code__isnull=False).filter(zammad_systemcode__isnull=False)
            for indicator in indicators:
                dataset = {
                    'indicatorCode': indicator.ias_code,
                    'series': []
                }
                for system in systems:
                    data = forming_data_by_gis_for_iac(zammad_systemcode=system.zammad_systemcode,
                                                       date=get_date(),
                                                       indicator=indicator)
                    dataset['series'].append(system.generate_series(value=data, times=time))
                datasets.append(dataset)
            data_for_iac['body']['datasets'] = datasets

        return data_for_iac

    except (SyntaxError, ConnectionError):
        raise
