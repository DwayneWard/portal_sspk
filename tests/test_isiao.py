import pytest
from rest_framework import status
from rest_framework.test import APIClient

from eva.isiao.serializers import GISSerializer, IndicatorSerializer


@pytest.mark.django_db
class TestISIAOAPIViews:

    def test_get_gis_unauthorized(self):

        client = APIClient()
        response = client.get('/eva/isiao/gis/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_gis_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/eva/isiao/gis/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_gis_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/eva/isiao/gis/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_gis_authorized_admin(self, admin_client):

        response = admin_client.get('/eva/isiao/gis/')

        assert response.status_code == status.HTTP_200_OK

    def test_create_gis_unauthorized(self):

        client = APIClient()
        response = client.post('/eva/isiao/gis/create/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_gis_authorized_user(self, simple_user_with_tools_client):

        data = {
            'full_name': 'string',
            'short_name': 'string',
            'dashboard_code': 'string',
            'zammad_systemcode': 2147483647
        }

        response = simple_user_with_tools_client.post(
            '/eva/isiao/gis/create/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_gis_authorized_eva(self, admin_eva_client):

        data = {
            'full_name': 'string',
            'short_name': 'string',
            'dashboard_code': 'string',
            'zammad_systemcode': 2147483647
        }

        response = admin_eva_client.post(
            '/eva/isiao/gis/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == data['full_name']
        assert response.data['short_name'] == data['short_name']
        assert response.data['dashboard_code'] == data['dashboard_code']
        assert response.data['zammad_systemcode'] == data['zammad_systemcode']

    def test_create_gis_authorized_admin(self, admin_client):

        data = {
            'full_name': 'string',
            'short_name': 'string',
            'dashboard_code': 'string',
            'zammad_systemcode': 2147483641
        }

        response = admin_client.post(
            '/eva/isiao/gis/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == data['full_name']
        assert response.data['short_name'] == data['short_name']
        assert response.data['dashboard_code'] == data['dashboard_code']
        assert response.data['zammad_systemcode'] == data['zammad_systemcode']

    def test_detail_gis_unauthorized(self, gis):

        client = APIClient()
        response = client.get(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_detail_gis_authorized_user(self, gis, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_detail_gis_authorized_eva(self, gis, admin_eva_client):

        response = admin_eva_client.get(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == GISSerializer(gis).data

    def test_detail_gis_authorized_admin(self, gis, admin_client):

        response = admin_client.get(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == GISSerializer(gis).data

    def test_put_gis_unauthorized(self, gis):

        data = {
            'full_name': 'Put_fullname',
            "short_name": gis.short_name,
            "dashboard_code": gis.dashboard_code,
            "zammad_systemcode": gis.zammad_systemcode
        }

        client = APIClient()
        response = client.put(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_gis_authorized_user(self, gis, simple_user_with_tools_client):

        data = {
            'full_name': 'Put_fullname',
            "short_name": gis.short_name,
            "dashboard_code": gis.dashboard_code,
            "zammad_systemcode": gis.zammad_systemcode
        }

        response = simple_user_with_tools_client.put(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_gis_authorized_eva(self, gis, admin_eva_client):

        data = {
            'full_name': 'Put_fullname',
            "short_name": gis.short_name,
            "dashboard_code": gis.dashboard_code,
            "zammad_systemcode": gis.zammad_systemcode
        }

        response = admin_eva_client.put(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['full_name'] == data['full_name']
        assert response.json()['short_name'] == data['short_name']
        assert response.json()['dashboard_code'] == data['dashboard_code']
        assert response.json()['zammad_systemcode'] == data['zammad_systemcode']

    def test_put_gis_authorized_admin(self, gis, admin_client):

        data = {
            'full_name': 'Put_fullname',
            "short_name": gis.short_name,
            "dashboard_code": gis.dashboard_code,
            "zammad_systemcode": gis.zammad_systemcode
        }

        response = admin_client.put(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['full_name'] == data['full_name']
        assert response.json()['short_name'] == data['short_name']
        assert response.json()['dashboard_code'] == data['dashboard_code']
        assert response.json()['zammad_systemcode'] == data['zammad_systemcode']

    def test_patch_gis_unauthorized(self, gis):

        data = {
            'zammad_systemcode': 121,
        }

        client = APIClient()
        response = client.patch(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_gis_authorized_user(self, gis, simple_user_with_tools_client):

        data = {
            'zammad_systemcode': 121,
        }

        response = simple_user_with_tools_client.patch(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_gis_authorized_eva(self, gis, admin_eva_client):

        data = {
            'zammad_systemcode': 121,
        }

        response = admin_eva_client.patch(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['zammad_systemcode'] == data['zammad_systemcode']

    def test_patch_gis_authorized_admin(self, gis, admin_client):

        data = {
            'zammad_systemcode': 121,
        }

        response = admin_client.patch(
            f'/eva/isiao/gis/{gis.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['zammad_systemcode'] == data['zammad_systemcode']

    def test_delete_gis_unauthorized(self, gis):

        client = APIClient()
        response = client.delete(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_gis_authorized_user(self, gis, simple_user_with_tools_client):

        response = simple_user_with_tools_client.delete(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_gis_authorized_eva(self, gis, admin_eva_client):

        response = admin_eva_client.delete(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_gis_authorized_admin(self, gis, admin_client):

        response = admin_client.delete(f'/eva/isiao/gis/{gis.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_indicators_unauthorized(self):

        client = APIClient()
        response = client.get('/eva/isiao/indicators/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_indicators_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/eva/isiao/indicators/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_indicators_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/eva/isiao/indicators/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_indicators_authorized_admin(self, admin_client):

        response = admin_client.get('/eva/isiao/indicators/')

        assert response.status_code == status.HTTP_200_OK

    def test_create_indicator_unauthorized(self):

        client = APIClient()
        response = client.post('/eva/isiao/indicators/create/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_indicator_authorized_user(self, simple_user_with_tools_client):

        data = {
            'full_name': 'string',
            'ias_code': 'string',
            'periodicity': 'day',
            'zammad_queryset': 'string'
        }

        response = simple_user_with_tools_client.post(
            '/eva/isiao/indicators/create/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_indicator_authorized_eva(self, admin_eva_client):

        data = {
            'full_name': 'string',
            'ias_code': 'string',
            'periodicity': 'day',
            'zammad_queryset': 'string'
        }

        response = admin_eva_client.post(
            '/eva/isiao/indicators/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == data['full_name']
        assert response.data['ias_code'] == data['ias_code']
        assert response.data['periodicity'] == data['periodicity']
        assert response.data['zammad_queryset'] == data['zammad_queryset']

    def test_create_indicator_authorized_admin(self, admin_client):

        data = {
            'full_name': 'string',
            'ias_code': 'string',
            'periodicity': 'day',
            'zammad_queryset': 'string'
        }

        response = admin_client.post(
            '/eva/isiao/indicators/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == data['full_name']
        assert response.data['ias_code'] == data['ias_code']
        assert response.data['periodicity'] == data['periodicity']
        assert response.data['zammad_queryset'] == data['zammad_queryset']

    def test_detail_indicator_unauthorized(self, indicator):

        client = APIClient()
        response = client.get(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_detail_indicator_authorized_user(self, indicator, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_detail_indicator_authorized_eva(self, indicator, admin_eva_client):

        response = admin_eva_client.get(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == IndicatorSerializer(indicator).data

    def test_detail_indicator_authorized_admin(self, indicator, admin_client):

        response = admin_client.get(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == IndicatorSerializer(indicator).data

    def test_put_indicator_unauthorized(self, indicator):

        data = {
            'full_name': 'Put_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        client = APIClient()
        response = client.put(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_indicator_authorized_user(self, indicator, simple_user_with_tools_client):

        data = {
            'full_name': 'Put_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        response = simple_user_with_tools_client.put(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_indicator_authorized_eva(self, indicator, admin_eva_client):

        data = {
            'full_name': 'Put_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        response = admin_eva_client.put(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['full_name'] == data['full_name']
        assert response.json()['ias_code'] == data['ias_code']
        assert response.json()['periodicity'] == data['periodicity']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']

    def test_put_indicator_authorized_admin(self, indicator, admin_client):

        data = {
            'full_name': 'Put_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        response = admin_client.put(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['full_name'] == data['full_name']
        assert response.json()['ias_code'] == data['ias_code']
        assert response.json()['periodicity'] == data['periodicity']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']

    def test_patch_indicator_unauthorized(self, indicator):

        data = {
            'full_name': 'Patch_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        client = APIClient()
        response = client.patch(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_indicator_authorized_user(self, indicator, simple_user_with_tools_client):

        data = {
            'full_name': 'Patch_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        response = simple_user_with_tools_client.patch(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_indicator_authorized_eva(self, indicator, admin_eva_client):

        data = {
            'full_name': 'Patch_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        response = admin_eva_client.patch(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['full_name'] == data['full_name']
        assert response.json()['ias_code'] == data['ias_code']
        assert response.json()['periodicity'] == data['periodicity']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']

    def test_patch_indicator_authorized_admin(self, indicator, admin_client):

        data = {
            'full_name': 'Patch_fullname',
            'ias_code': indicator.ias_code,
            'periodicity': indicator.periodicity,
            'zammad_queryset': indicator.zammad_queryset
        }

        response = admin_client.patch(
            f'/eva/isiao/indicators/{indicator.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['full_name'] == data['full_name']
        assert response.json()['ias_code'] == data['ias_code']
        assert response.json()['periodicity'] == data['periodicity']
        assert response.json()['zammad_queryset'] == data['zammad_queryset']

    def test_delete_indicator_unauthorized(self, indicator):

        client = APIClient()
        response = client.delete(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_indicator_authorized_user(self, indicator, simple_user_with_tools_client):

        response = simple_user_with_tools_client.delete(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_indicator_authorized_eva(self, indicator, admin_eva_client):

        response = admin_eva_client.delete(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_indicator_authorized_admin(self, indicator, admin_client):

        response = admin_client.delete(f'/eva/isiao/indicators/{indicator.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
