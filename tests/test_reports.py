import pytest
from redis.exceptions import ConnectionError as DoesNotConnectRedis
from rest_framework import status
from rest_framework.test import APIClient

from eva.reports.serializers import CategorySerializer
from eva.reports.utils import create_report_key_in_redis_db


@pytest.mark.django_db
class TestReportsAPIViews:

    def test_get_reports_unauthorized(self):

        client = APIClient()
        response = client.get('/eva/reports/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_reports_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/eva/reports/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_reports_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/eva/reports/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_reports_authorized_admin(self, admin_client):

        response = admin_client.get('/eva/reports/')

        assert response.status_code == status.HTTP_200_OK

    def test_create_reports_unauthorized(self):

        client = APIClient()
        response = client.post('/eva/reports/create/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_reports_authorized_user(self, simple_user, category, simple_user_with_tools_client):

        data = {
            'serial_number': 1,
            'name': 'string',
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = simple_user_with_tools_client.post(
            '/eva/reports/create/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_reports_authorized_eva(self, simple_user, category, admin_eva_client):

        data = {
            'serial_number': 1,
            'name': 'string',
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_eva_client.post(
            '/eva/reports/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_reports_authorized_admin(self, simple_user, category, admin_client):

        data = {
            'serial_number': 1,
            'name': 'string',
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_client.post(
            '/eva/reports/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_categories_unauthorized(self):

        client = APIClient()
        response = client.get('/eva/reports_categories/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_categories_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/eva/reports_categories/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_categories_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/eva/reports_categories/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_categories_authorized_admin(self, admin_client):

        response = admin_client.get('/eva/reports_categories/')

        assert response.status_code == status.HTTP_200_OK

    def test_create_categories_unauthorized(self):

        client = APIClient()
        response = client.post('/eva/reports_categories/create/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_categories_authorized_user(self, simple_user_with_tools_client):

        data = {
            'serial_number': 1,
            'name': 'string',
        }

        response = simple_user_with_tools_client.post(
            '/eva/reports_categories/create/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_categories_authorized_eva(self, admin_eva_client):

        data = {
            'serial_number': 1,
            'name': 'string',
        }

        response = admin_eva_client.post(
            '/eva/reports_categories/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_categories_authorized_admin(self, admin_client):

        data = {
            'serial_number': 1,
            'name': 'string',
        }

        response = admin_client.post(
            '/eva/reports_categories/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_detail_category_unauthorized(self, category):

        client = APIClient()
        response = client.get(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_detail_category_authorized_user(self, category, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_detail_category_authorized_eva(self, category, admin_eva_client):

        response = admin_eva_client.get(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == CategorySerializer(category).data

    def test_detail_category_authorized_admin(self, category, admin_client):

        response = admin_client.get(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == CategorySerializer(category).data

    def test_put_category_unauthorized(self, category):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        client = APIClient()
        response = client.put(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_category_authorized_user(self, category, simple_user_with_tools_client):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        response = simple_user_with_tools_client.put(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_category_authorized_eva(self, category, admin_eva_client):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        response = admin_eva_client.put(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']

    def test_put_category_authorized_admin(self, category, admin_client):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        response = admin_client.put(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']

    def test_patch_category_unauthorized(self, category):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        client = APIClient()
        response = client.patch(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_category_authorized_user(self, category, simple_user_with_tools_client):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        response = simple_user_with_tools_client.patch(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_category_authorized_eva(self, category, admin_eva_client):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        response = admin_eva_client.patch(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']

    def test_patch_category_authorized_admin(self, category, admin_client):

        data = {
            'serial_number': category.serial_number,
            'name': 'Test'
        }

        response = admin_client.patch(
            f'/eva/reports_categories/{category.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']

    def test_get_report_unauthorized(self, reports):

        client = APIClient()
        response = client.get(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_report_authorized_user(self, reports, redis_client, simple_user_with_tools_client, mocker):

        fake_data = {
            'columns': ['col1', 'col2'],
            'results': [[1, 2], [3, 4]]
        }

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)
        mock_json = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)

        response = simple_user_with_tools_client.get(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'details': 'Ключ записан в редис'}

        response_invalid_pk = simple_user_with_tools_client.get('/eva/reports/666/')

        assert response_invalid_pk.status_code == status.HTTP_404_NOT_FOUND
        assert response_invalid_pk.json() == {'detail': 'Отчета с таким номером не существует'}

        mock_json.side_effect = DoesNotConnectRedis('')

        response_connection = simple_user_with_tools_client.get(f'/eva/reports/{reports.pk}/')

        assert response_connection.status_code == status.HTTP_502_BAD_GATEWAY
        assert response_connection.json() == {'detail': 'Не могу подключиться к redis. '
                                                        'Сообщите администратору системы или в отдел сопровождения СПО'}

        mock_json.reset_mock()
        mock_redis.reset_mock()

    def test_get_report_authorized_eva(self, reports, redis_client, admin_eva_client, mocker):

        fake_data = {
            'columns': ['col1', 'col2'],
            'results': [[1, 2], [3, 4]]
        }

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)
        mock_json = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)

        response = admin_eva_client.get(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'details': 'Ключ записан в редис'}

        response_invalid_pk = admin_eva_client.get('/eva/reports/666/')

        assert response_invalid_pk.status_code == status.HTTP_404_NOT_FOUND
        assert response_invalid_pk.json() == {'detail': 'Отчета с таким номером не существует'}

        mock_json.side_effect = SyntaxError('')

        response_syntax = admin_eva_client.get(f'/eva/reports/{reports.pk}/')

        assert response_syntax.status_code == status.HTTP_404_NOT_FOUND
        assert response_syntax.json() == {'detail': 'Ошибка в запросе на получение отчета. Обратитесь к администратору.'}

        mock_json.reset_mock()
        mock_redis.reset_mock()

    def test_get_report_authorized_admin(self, reports, redis_client, admin_client, mocker):

        fake_data = {
            'columns': ['col1', 'col2'],
            'results': [[1, 2], [3, 4]]
        }

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)
        mock_json = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)

        response = admin_client.get(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'details': 'Ключ записан в редис'}

        response_invalid_pk = admin_client.get('/eva/reports/666/')

        assert response_invalid_pk.status_code == status.HTTP_404_NOT_FOUND
        assert response_invalid_pk.json() == {'detail': 'Отчета с таким номером не существует'}

        mock_json.side_effect = SyntaxError('')

        response_syntax = admin_client.get(f'/eva/reports/{reports.pk}/')

        assert response_syntax.status_code == status.HTTP_404_NOT_FOUND
        assert response_syntax.json() == {'detail': 'Ошибка в запросе на получение отчета. Обратитесь к администратору.'}

        mock_json.reset_mock()
        mock_redis.reset_mock()

    def test_put_report_unauthorized(self, reports):

        client = APIClient()
        response = client.put(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_report_authorized_user(self, reports, category, simple_user, simple_user_with_tools_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = simple_user_with_tools_client.put(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_report_authorized_eva(self, reports, category, simple_user, admin_eva_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_eva_client.put(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']
        assert response.json()['category'] == data['category']
        assert response.json()['users'] == data['users']

    def test_put_report_authorized_admin(self, reports, category, simple_user, admin_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_client.put(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']
        assert response.json()['category'] == data['category']
        assert response.json()['users'] == data['users']

    def test_patch_report_unauthorized(self, reports):

        client = APIClient()
        response = client.patch(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_report_authorized_user(self, reports, category, simple_user, simple_user_with_tools_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = simple_user_with_tools_client.patch(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_report_authorized_eva(self, reports, category, simple_user, admin_eva_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_eva_client.patch(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']
        assert response.json()['category'] == data['category']
        assert response.json()['users'] == data['users']

    def test_patch_report_authorized_admin(self, reports, category, simple_user, admin_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_client.patch(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['serial_number'] == data['serial_number']
        assert response.json()['name'] == data['name']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']
        assert response.json()['category'] == data['category']
        assert response.json()['users'] == data['users']

    def test_get_json_report_unauthorized(self, reports):

        client = APIClient()
        response = client.get(f'/eva/reports/{reports.pk}/json/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_json_report_authorized_user(self, reports, redis_client, simple_user_with_tools_client, mocker):

        fake_data = {'results': 'results', 'columns': 'columns'}

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)
        mock_data = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)

        create_report_key_in_redis_db(reports)

        response = simple_user_with_tools_client.get(f'/eva/reports/{reports.pk}/json/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == fake_data

        response_type = simple_user_with_tools_client.get('/eva/reports/666/json/')

        assert response_type.status_code == status.HTTP_404_NOT_FOUND
        assert response_type.json() == {'details': 'Ключ в редис не найден'}

        mock_data.reset_mock()
        mock_redis.reset_mock()

    def test_get_json_report_authorized_eva(self, reports, redis_client, admin_eva_client, mocker):

        fake_data = {'results': 'results', 'columns': 'columns'}

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)
        mock_data = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)

        create_report_key_in_redis_db(reports)

        response = admin_eva_client.get(f'/eva/reports/{reports.pk}/json/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == fake_data

        response_type = admin_eva_client.get('/eva/reports/666/json/')

        assert response_type.status_code == status.HTTP_404_NOT_FOUND
        assert response_type.json() == {'details': 'Ключ в редис не найден'}

        mock_data.reset_mock()
        mock_redis.reset_mock()

    def test_get_json_report_authorized_admin(self, reports, redis_client, admin_client, mocker):

        fake_data = {'results': 'results', 'columns': 'columns'}

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)
        mock_data = mocker.patch('eva.reports.utils.forming_data_for_single_report', return_value=fake_data)

        create_report_key_in_redis_db(reports)

        response = admin_client.get(f'/eva/reports/{reports.pk}/json/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == fake_data

        response_type = admin_client.get('/eva/reports/666/json/')

        assert response_type.status_code == status.HTTP_404_NOT_FOUND
        assert response_type.json() == {'details': 'Ключ в редис не найден'}

        mock_data.reset_mock()
        mock_redis.reset_mock()

    def test_get_file_report_unauthorized(self, reports):

        client = APIClient()
        response = client.get(f'/eva/reports/{reports.pk}/json/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_file_report_authorized_user(self, redis_client, simple_user_with_tools_client, mocker,
                                             fake_data_in_redis_for_download):

        serial_number, fake_data = fake_data_in_redis_for_download

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)

        response_xlsx = simple_user_with_tools_client.get(f'/eva/reports/{serial_number}/xlsx/')

        assert response_xlsx.status_code == status.HTTP_200_OK

        response_csv = simple_user_with_tools_client.get(f'/eva/reports/{serial_number}/csv/')

        assert response_csv.status_code == status.HTTP_200_OK

        mock_redis.side_effect = TypeError()

        response_type_xlsx = simple_user_with_tools_client.get(f'/eva/reports/{serial_number}/xlsx/')

        assert response_type_xlsx.status_code == status.HTTP_404_NOT_FOUND
        assert response_type_xlsx.json() == {'detail': 'Необходимо повторно сгенерировать отчет'}

        response_type_csv = simple_user_with_tools_client.get(f'/eva/reports/{serial_number}/csv/')

        assert response_type_csv.status_code == status.HTTP_404_NOT_FOUND
        assert response_type_csv.json() == {'detail': 'Необходимо повторно сгенерировать отчет'}

    def test_get_file_report_authorized_eva(self, redis_client, admin_eva_client, mocker,
                                            fake_data_in_redis_for_download):

        serial_number, fake_data = fake_data_in_redis_for_download

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)

        response_xlsx = admin_eva_client.get(f'/eva/reports/{serial_number}/xlsx/')

        assert response_xlsx.status_code == status.HTTP_200_OK

        response_csv = admin_eva_client.get(f'/eva/reports/{serial_number}/csv/')

        assert response_csv.status_code == status.HTTP_200_OK

        mock_redis.side_effect = TypeError()

        response_type_xlsx = admin_eva_client.get(f'/eva/reports/{serial_number}/xlsx/')

        assert response_type_xlsx.status_code == status.HTTP_404_NOT_FOUND
        assert response_type_xlsx.json() == {'detail': 'Необходимо повторно сгенерировать отчет'}

        response_type_csv = admin_eva_client.get(f'/eva/reports/{serial_number}/csv/')

        assert response_type_csv.status_code == status.HTTP_404_NOT_FOUND
        assert response_type_csv.json() == {'detail': 'Необходимо повторно сгенерировать отчет'}

    def test_get_file_report_authorized_admin(self, redis_client, admin_client, mocker,
                                              fake_data_in_redis_for_download):

        serial_number, fake_data = fake_data_in_redis_for_download

        mock_redis = mocker.patch('eva.reports.utils.get_connect_with_redis', return_value=redis_client)

        response_xlsx = admin_client.get(f'/eva/reports/{serial_number}/xlsx/')

        assert response_xlsx.status_code == status.HTTP_200_OK

        response_csv = admin_client.get(f'/eva/reports/{serial_number}/csv/')

        assert response_csv.status_code == status.HTTP_200_OK

        mock_redis.side_effect = TypeError()

        response_type_xlsx = admin_client.get(f'/eva/reports/{serial_number}/xlsx/')

        assert response_type_xlsx.status_code == status.HTTP_404_NOT_FOUND
        assert response_type_xlsx.json() == {'detail': 'Необходимо повторно сгенерировать отчет'}

        response_type_csv = admin_client.get(f'/eva/reports/{serial_number}/csv/')

        assert response_type_csv.status_code == status.HTTP_404_NOT_FOUND
        assert response_type_csv.json() == {'detail': 'Необходимо повторно сгенерировать отчет'}

    def test_delete_report_unauthorized(self, reports):

        client = APIClient()
        response = client.delete(f'/eva/reports/{reports.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_report_authorized_user(self, reports, category, simple_user, simple_user_with_tools_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = simple_user_with_tools_client.delete(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_report_authorized_eva(self, reports, category, simple_user, admin_eva_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_eva_client.delete(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_report_authorized_admin(self, reports, category, simple_user, admin_client):

        data = {
            'serial_number': reports.serial_number,
            'name': reports.name,
            'zammad_queryset': 'string',
            'category': category.serial_number,
            'users': [simple_user.id]
        }

        response = admin_client.delete(
            f'/eva/reports/{reports.pk}/',
            data=data,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_category_unauthorized(self, category):

        client = APIClient()
        response = client.delete(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_category_authorized_user(self, category, simple_user_with_tools_client):

        response = simple_user_with_tools_client.delete(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_authorized_eva(self, category, admin_eva_client):

        response = admin_eva_client.delete(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_category_authorized_admin(self, category, admin_client):

        response = admin_client.delete(f'/eva/reports_categories/{category.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
