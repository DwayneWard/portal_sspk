import datetime

import psycopg2


def get_cursor_from_zammad_db(db: str, host: str, port: str, user: str, password: str, queryset: str):
    """
    Осуществляет к подключение к БД Zammad и обрабатывает SQL-запрос.

    :param db: Имя БД, к которой необходимо подлкючиться
    :param host: Хост, на котором расположена БД
    :param port: Порт, который необходимо использовать для подключения
    :param user: Имя пользователя БД
    :param password: Пароль пользователя БД
    :param queryset: SQL-запрос, который необходимо выполнить
    :return: В случае успешного выполнения запроса возвращает курсор с данными по выполненному запросу.
    В случае ошибки в SQL-запроса должен делать raise SyntaxError
    В случае ошибки в подключении должен делать raise ConnectionError
    """
    with psycopg2.connect(
            database=db,
            host=host,
            port=port,
            user=user,
            password=password) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(queryset)
            return cursor
        except psycopg2.errors.SyntaxError:
            raise SyntaxError
        except psycopg2.errors.OperationalError:
            raise ConnectionError


def get_date(date: datetime.date = None) -> datetime:
    """
    Функция для получения вчерашней даты относительно сегодня или же переданной даты.
    Используется для задач Celery.

    :param date: Параметр даты, относительно которого нужно получить вчерашнюю дату.

    Возвращает обьект datetime.
    """

    if not date:
        return datetime.date.today() - datetime.timedelta(days=1)
    else:
        return date - datetime.timedelta(days=1)
