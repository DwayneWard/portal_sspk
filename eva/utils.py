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
        # TODO: Заменить Exception на конкретную ошибку в ходе тестирования функциональности.
        except Exception:
            raise SyntaxError


def get_date(month: bool = False, week: bool = False) -> str:
    """
    Функция для получения даты. Может отдавать вчерашний день, порядковый номер недели или первый день месяца.
    Используется для задач Celery.

    :param month: Логический параметр. Если True - отдает первое число месяца.
    :param week: Логический параметр. Если True - отдает какая неделя в году.

    Если оба параметра month и week имеют значение False, то отдает вчерашний день.
    """
    if month:
        return datetime.date.today().strftime('%Y-%m')
    if week:
        return f'W{datetime.date.today().isocalendar().week}'
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
