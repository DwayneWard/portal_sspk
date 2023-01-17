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
    :return: В случае успешного выполнения запроса возвращает курсор с данными по выполненному запросу. В случае ошибки в SQL-запроса должен делать raise SyntaxError
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
