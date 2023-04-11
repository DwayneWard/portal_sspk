import pytest
from factories import (AdminEvaFactory, AdminFactory, CategoryFactory, EvaToolFactory, GISFactory,
                       IndicatorFactory, PanelToolFactory, ReportsFactory, SimpleUserFactory, TaskResultFactory,
                       ToolsFactory)
from pytest_factoryboy import register
from redis import Redis
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

register(AdminEvaFactory, 'admin_eva')
register(AdminFactory, 'admin')
register(CategoryFactory, 'category')
register(EvaToolFactory, 'eva_tool')
register(GISFactory, 'gis')
register(IndicatorFactory, 'indicator')
register(PanelToolFactory, 'panel_tool')
register(ReportsFactory, 'reports')
register(SimpleUserFactory, 'simple_user')
register(TaskResultFactory, 'task_result')
register(ToolsFactory, 'tools')


class UserWithToolsFactory:
    @staticmethod
    def make_user_with_tools(tools):
        user = SimpleUserFactory.create(username='test_user')
        for tool in tools:
            user.tools.add(tool)
        return user


@pytest.fixture
def admin_client():
    client = APIClient()
    user = AdminFactory.create(username='test_admin')

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client


@pytest.fixture
def admin_eva_client():
    client = APIClient()
    user = AdminEvaFactory.create(username='test_eva')

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client


@pytest.fixture
def simple_user_with_tools_client():
    client = APIClient()
    tools = ToolsFactory.create_batch(3)
    user = UserWithToolsFactory.make_user_with_tools(tools)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client


@pytest.fixture(scope='function')
def redis_client():
    # Создание тестового Redis клиента с использованием базы данных номер 1
    client = Redis(host='localhost', port=6379, db=1)
    yield client
    # Очистка тестовой базы данных после каждого теста
    client.flushdb()
    client.close()


@pytest.fixture()
def fake_data_in_redis(redis_client, reports):
    import json

    fake_data = {'results': 'results', 'columns': 'columns'}
    redis_client.set(f'{reports.serial_number}', json.dumps(fake_data, ensure_ascii=False, default=str))

    return [reports.serial_number, fake_data]


@pytest.fixture()
def fake_data_in_redis_for_download(redis_client, reports):
    import json

    fake_data = {'columns': ['id', 'name', 'age'], 'results': [[1, 'John', 25], [2, 'Mary', 35]]}
    redis_client.set(f'{reports.serial_number}', json.dumps(fake_data, ensure_ascii=False, default=str))

    return [reports.serial_number, fake_data]


@pytest.fixture
def mock_cursor(mocker, monkeypatch):
    mock_cursor = mocker.Mock()
    mock_cursor.description = [('id',), ('name',)]
    mock_cursor.fetchall.return_value = [(1, 'John'), (2, 'Jane')]
    monkeypatch.setattr('eva.reports.utils.get_cursor_from_zammad_db', lambda *args, **kwargs: mock_cursor)
