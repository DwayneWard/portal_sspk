import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestControlPanelAPIViews:

    def test_get_check_result_unauthorized(self):

        client = APIClient()
        response = client.get('/control_panel/check_results/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_check_result_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/control_panel/check_results/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_check_result_authorized_eva(self, task_result, admin_eva_client):

        response = admin_eva_client.get('/control_panel/check_results/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_get_check_result_authorized_admin(self, task_result, admin_client):

        response = admin_client.get('/control_panel/check_results/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_get_resend_result_unauthorized(self):

        client = APIClient()
        response = client.get('/control_panel/resend_tasks/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_resend_result_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/control_panel/resend_tasks/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_resend_result_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/control_panel/resend_tasks/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_resend_result_authorized_admin(self, admin_client):

        response = admin_client.get('/control_panel/resend_tasks/')

        assert response.status_code == status.HTTP_200_OK
