from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('У пользователя обязательно должен быть логин')
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.role = 'user'
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.role = 'admin'
        user.save(using=self._db)
        return user
