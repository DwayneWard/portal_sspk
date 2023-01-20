import datetime
import json

import pandas
from django.http import JsonResponse
from redis import ConnectionPool, StrictRedis

from eva.reports.models import Reports
from eva.utils import get_cursor_from_zammad_db
from portal.settings import (CELERY_BROKER_URL, ZAMMAD_DB_HOST, ZAMMAD_DB_NAME,
                             ZAMMAD_DB_PASSWORD, ZAMMAD_DB_PORT,
                             ZAMMAD_DB_USER)

pool = ConnectionPool.from_url(CELERY_BROKER_URL)
redis = StrictRedis(connection_pool=pool)


def get_date(month: bool = False) -> datetime:
    """
    Функция для получения даты. Может отдавать вчерашний день или первый день месяца. Используется для задач Celery.

    :param month: Логический параметр. Если False - отдает вчерашнюю дату, если True - отдает первое число месяца.
    """

    if month:
        return datetime.date.today().strftime('%Y-%m')
    else:
        return datetime.date.today() - datetime.timedelta(days=1)


def forming_data_for_single_report(queryset: str):
    """
    Формирует данные по требуемому отчету на основе queryset.

    :param queryset: SQL-запрос, который берется из Отчет -> поле zammad_queryset.
    :return: В случае успешного выполнения - данные из БД Zammad, в случае SyntaxError: Сообщение об ошибке.
    """

    try:
        cursor = get_cursor_from_zammad_db(
            db=ZAMMAD_DB_NAME,
            host=ZAMMAD_DB_HOST,
            port=ZAMMAD_DB_PORT,
            user=ZAMMAD_DB_USER,
            password=ZAMMAD_DB_PASSWORD,
            queryset=queryset,
        )
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        return {'results': results, 'columns': columns}
    except SyntaxError:
        return {'detail': 'При формировании отчета возникла ошибка. '
                          'Обратитесь к администратору системы.'}  # TODO: Возможно не работает. Нужно проверить


def create_report_key_in_redis_db(redis_db: StrictRedis, report: Reports, key_expire_time: int = 600) -> None:
    """
    Создает ключ с данными по отчету после генерации в редис с заданным временм жизни.

    :param redis_db: БД Редис, в которую необходимо добавить ключ
    :param key_expire_time: Время жизни ключа внутри redis. По умолчанию равно 10 минутам.
    :param report: Отчет, для которого необходимо сохранить временный ключ
    :return: None
    """

    # TODO: Добавить проверку на то, что отчет есть в БД.
    data_from_zammad_db = forming_data_for_single_report(report.zammad_queryset)
    redis_db.set(f"{report.serial_number}", json.dumps(data_from_zammad_db, ensure_ascii=False))
    redis_db.expire(f"{report.serial_number}", key_expire_time)


def generate_content_type_for_download(type_of_header: str):
    """
    Генерирует content type для хедера HTTP запроса.

    :param type_of_header: Тип файла для генерации. Доступны файлы csv или xlsx
    :return: content type в нужном формате в случае успеха.
    В случае, если предан неверный формат файла возвращает JsonResponse
    """

    if type_of_header == 'xlsx':
        content_type = 'application/vnd.ms-excel'
        return content_type
    elif type_of_header == 'csv':
        content_type = 'text/csv'
        return content_type
    else:
        return JsonResponse({'detail': 'Передан неверный формат файла. Передайте csv или xlsx'})


def convert_data_to_docs_format(response, file_extension: str, redis_data: dict) -> None:
    """
    Преобразует данные в нужный формат (csv или xlsx) и записывает их в response.

    :param response: response в который необходимо записать данные
    :param file_extension: Необходимое расширение файлов
    :param redis_data: Данные, полученные из ключа redis
    :return: None
    """

    data_for_convert = pandas.DataFrame(redis_data['results'], columns=redis_data['columns'])
    if file_extension == 'csv':
        data_for_convert.to_csv(response, sep=';', index=False)
    elif file_extension == 'xlsx':
        data_for_convert.to_excel(response, index=False, engine='xlsxwriter')
