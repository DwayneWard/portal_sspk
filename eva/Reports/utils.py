import psycopg2

from eva.Reports.models import Reports
from eva.utils import get_cursor_from_zammad_db
from portal.settings import (ZAMMAD_DB_HOST, ZAMMAD_DB_NAME,
                             ZAMMAD_DB_PASSWORD, ZAMMAD_DB_PORT,
                             ZAMMAD_DB_USER)


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
        result = cursor.fetcall()
        return result
    except SyntaxError:
        return {'detail': 'При формировании отчета возникла ошибка. '
                          'Обратитесь к администратору системы.'}  # TODO: Возможно не работает. Нужно проверить
