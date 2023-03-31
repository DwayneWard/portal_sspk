from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserRoles


class IsUser(BasePermission):
    """
    Разрешение для пользователей.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_user == UserRoles.USER


class IsAdminOrAdminEVA(BasePermission):
    """
    Разрешение для администраторов или администраторов ЕВА.
    """

    def has_permission(self, request, view):
        # Получаем авторизованного пользователя из JWT токена
        auth = JWTAuthentication()
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is not None:
            user, token = user_auth_tuple
        else:
            return False

        # Извлекаем из токена информацию о роли пользователя
        role = user.role

        # Проверяем, что пользователь аутентифицирован и имеет необходимую роль
        return user.is_authenticated and (role == UserRoles.ADMIN or role == UserRoles.ADMIN_EVA)


class IsAdminAndAdminEVAorUser(BasePermission):
    """
    Разрешение для администраторов, администраторов ЕВА или пользователей.
    """

    def has_permission(self, request, view):
        # Получаем авторизованного пользователя из JWT токена
        auth = JWTAuthentication()
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is not None:
            user, token = user_auth_tuple
        else:
            return False

        # Извлекаем из токена информацию о роли пользователя
        role = user.role

        if user.is_authenticated:
            if role == UserRoles.ADMIN or role == UserRoles.ADMIN_EVA:
                return True
            if role == UserRoles.USER:
                if request.method == 'GET':
                    return True
        else:
            return False
