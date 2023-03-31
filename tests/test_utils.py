import datetime
import json
import random

import pytest

from eva.isiao.utils import convert_date, generate_data, get_name_task_to_db
from eva.reports.utils import (create_report_key_in_redis_db, forming_data_for_single_report,
                               generate_content_type_for_download, get_data_from_redis)
from eva.utils import get_date


@pytest.mark.django_db
class TestUtilsEVA:

    date = datetime.date(2022, 1, 15)

    def test_get_date(self):

        random_date = self.date - datetime.timedelta(days=random.randint(1, 31))

        assert get_date() == datetime.date.today() - datetime.timedelta(days=1)
        assert get_date(random_date.isoformat()) == random_date - datetime.timedelta(days=1)

    def test_convert_date(self):

        assert convert_date(self.date) == (f'{self.date.year}-{self.date.month}-{self.date.day}', 'day', self.date)
        assert convert_date(self.date, 'day') == (f'{self.date.year}-{self.date.month}-{self.date.day}', 'day', self.date)
        assert convert_date(self.date, 'week') == (f'{self.date.year}-W{self.date.isocalendar().week}', 'week', self.date)
        assert convert_date(self.date, 'month') == (f'{self.date.year}-{self.date.month}', 'month', self.date)
        assert convert_date(self.date, 'quarter') == (f'{self.date.year}-Q4', 'quarter', self.date)
        assert convert_date(self.date, 'half_year') == (f'{self.date.year}-H2', 'half_year', self.date)
        assert convert_date(self.date, 'year') == (f'{self.date.year}', 'year', self.date)

    def test_get_name_task_to_db(self):

        assert get_name_task_to_db('day') == 'Ежедневная'
        assert get_name_task_to_db('week') == 'Еженедельная'
        assert get_name_task_to_db('month') == 'Ежемесячная'
        assert get_name_task_to_db('quarter') == 'Ежеквартальная'
        assert get_name_task_to_db('half_year') == 'Полугодовая'
        assert get_name_task_to_db('year') == 'Ежегодная'

    def test_generate_data(self, indicator, gis, mocker):

        mock_int = mocker.patch('eva.isiao.utils.forming_data_by_gis_for_iac', return_value=10)

        data_day = generate_data(*convert_date(self.date, 'day'))

        assert data_day['body']['datasets'][0]['series'][0]['observation']['value'] == 10

        with pytest.raises((SyntaxError, ConnectionError)):
            mock_int.side_effect = SyntaxError
            generate_data(*convert_date(self.date, 'day'))
            mock_int.reset_mock()

        with pytest.raises((SyntaxError, ConnectionError)):
            mock_int.side_effect = ConnectionError
            generate_data(*convert_date(self.date, 'day'))
            mock_int.reset_mock()

        mock_int.reset_mock()

    def test_get_data_from_redis(self, fake_data_in_redis, redis_client, mocker):

        serial_number, fake_data = fake_data_in_redis

        mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)

        data_redis = get_data_from_redis(serial_number)

        assert data_redis == fake_data

    def test_generate_content_type_for_download(self):

        assert generate_content_type_for_download('xlsx') == 'application/vnd.ms-excel'
        assert generate_content_type_for_download('csv') == 'text/csv'
        content_type = generate_content_type_for_download('pdf').content.decode('utf-8')
        assert json.loads(content_type) == {'detail': 'Передан неверный формат файла. Передайте csv или xlsx'}

    def test_create_report_key_in_redis_db(self, reports, redis_client, mocker):

        fake_data = {'results': 'results', 'columns': 'columns'}

        mock_data = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)
        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)

        create_report_key_in_redis_db(reports)

        data = json.loads(redis_client.get(reports.serial_number).decode('utf-8'))

        assert data == fake_data

    def test_forming_data_for_single_report(self, mock_cursor):

        data_from_zammad = forming_data_for_single_report('fake_queryest')

        assert data_from_zammad == {'results': [(1, 'John'), (2, 'Jane')], 'columns': ['id', 'name']}
