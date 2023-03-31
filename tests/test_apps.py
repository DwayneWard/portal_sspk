import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAppsAPIViews:

    def test_get_apps_unauthorized(self):

        client = APIClient()
        response = client.get('/apps/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_apps_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/apps/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_apps_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/apps/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_apps_authorized_admin(self, admin_client):

        response = admin_client.get('/apps/')

        assert response.status_code == status.HTTP_200_OK
