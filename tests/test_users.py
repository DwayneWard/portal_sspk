import pytest
from factories import faker
from rest_framework import status
from rest_framework.test import APIClient

from authority.serializers import UserChangeSerializer


@pytest.mark.django_db
class TestUsersAPIViews:

    def test_get_users_unauthorized(self):

        client = APIClient()
        response = client.get('/auth/users/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_users_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/auth/users/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/auth/users/')

        assert response.status_code == status.HTTP_200_OK

    def test_get_users_authorized_admin(self, admin_client):

        response = admin_client.get('/auth/users/')

        assert response.status_code == status.HTTP_200_OK

    def test_create_user_unauthorized(self):

        client = APIClient()
        response = client.post('/auth/users/create/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_user_authorized_user(self, simple_user_with_tools_client):

        data = {
            'username': faker.unique.name(),
            'first_name': faker.unique.first_name(),
            'last_name': faker.unique.name(),
            'password': '12345678qwerty'
        }

        response = simple_user_with_tools_client.post(
            '/auth/users/create/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_user_authorized_eva(self, admin_eva_client):

        data = {
            'username': faker.unique.name(),
            'first_name': faker.unique.first_name(),
            'last_name': faker.unique.name(),
            'password': '12345678qwerty'
        }

        response = admin_eva_client.post(
            '/auth/users/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == data['username']
        assert response.data['first_name'] == data['first_name']
        assert response.data['last_name'] == data['last_name']

    def test_create_user_authorized_admin(self, admin_client):

        data = {
            'username': faker.unique.name(),
            'first_name': faker.unique.first_name(),
            'last_name': faker.unique.name(),
            'password': '12345678qwerty'
        }

        response = admin_client.post(
            '/auth/users/create/',
            data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == data['username']
        assert response.data['first_name'] == data['first_name']
        assert response.data['last_name'] == data['last_name']

    def test_detail_user_unauthorized(self, simple_user):

        client = APIClient()
        response = client.get(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_detail_user_authorized_user(self, simple_user, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_detail_user_authorized_eva(self, simple_user, admin_eva_client):

        response = admin_eva_client.get(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserChangeSerializer(simple_user).data

    def test_detail_user_authorized_admin(self, simple_user, admin_client):

        response = admin_client.get(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserChangeSerializer(simple_user).data

    def test_put_user_unauthorized(self, simple_user):

        data = {
            'username': 'Put_name',
        }

        client = APIClient()
        response = client.put(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_user_authorized_user(self, simple_user, simple_user_with_tools_client):

        data = {
            'username': 'Put_name',
        }

        response = simple_user_with_tools_client.put(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_user_authorized_eva(self, simple_user, admin_eva_client):

        data = {
            'username': 'Put_name',
            'first_name': simple_user.first_name,
            'last_name': simple_user.last_name,
        }

        response = admin_eva_client.put(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == data['username']
        assert response.json()['first_name'] == data['first_name']
        assert response.json()['last_name'] == data['last_name']

    def test_put_user_authorized_admin(self, simple_user, admin_client):

        data = {
            'username': 'Put_name',
            'first_name': simple_user.first_name,
            'last_name': simple_user.last_name,
        }

        response = admin_client.put(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == data['username']
        assert response.json()['first_name'] == data['first_name']
        assert response.json()['last_name'] == data['last_name']

    def test_patch_user_unauthorized(self, simple_user):

        data = {
            'username': 'Patch_name',
        }

        client = APIClient()
        response = client.patch(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_user_authorized_user(self, simple_user, simple_user_with_tools_client):

        data = {
            'username': 'Patch_name',
        }

        response = simple_user_with_tools_client.patch(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_user_authorized_eva(self, simple_user, admin_eva_client):

        data = {
            'username': 'Patch_name',
        }

        response = admin_eva_client.patch(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == data['username']

    def test_patch_user_authorized_admin(self, simple_user, admin_client):

        data = {
            'username': 'Patch_name',
        }

        response = admin_client.patch(
            f'/auth/users/{simple_user.pk}/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == data['username']

    def test_delete_user_unauthorized(self, simple_user):

        client = APIClient()
        response = client.delete(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_user_authorized_user(self, simple_user, simple_user_with_tools_client):

        response = simple_user_with_tools_client.delete(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_authorized_eva(self, simple_user, admin_eva_client):

        response = admin_eva_client.delete(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_user_authorized_admin(self, simple_user, admin_client):

        response = admin_client.delete(f'/auth/users/{simple_user.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_cabinet_user_unauthorized(self):

        client = APIClient()
        response = client.get('/auth/cabinet/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cabinet_user_authorized_user(self, simple_user_with_tools_client):

        response = simple_user_with_tools_client.get('/auth/cabinet/')

        assert response.status_code == status.HTTP_200_OK

    def test_cabinet_user_authorized_eva(self, admin_eva_client):

        response = admin_eva_client.get('/auth/cabinet/')

        assert response.status_code == status.HTTP_200_OK

    def test_cabinet_user_authorized_admin(self, admin_client):

        response = admin_client.get('/auth/cabinet/')

        assert response.status_code == status.HTTP_200_OK

    def test_login_incorrect_user(self):

        data = {
            'username': 'incorrect_user',
            'password': '12345678qwerty',
        }

        client = APIClient()
        response = client.post(
            '/auth/login/',
            data=data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_correct_user(self, simple_user):

        data = {
            'username': simple_user.username,
            'password': '12345678qwerty',
        }

        client = APIClient()

        response = client.post(
            '/auth/login/',
            data=data
        )

        assert response.status_code == status.HTTP_200_OK
