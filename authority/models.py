from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Permission, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from authority.managers import UserManager
from portal.models import Tools


class UserRoles:
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ADMIN_EVA = "admin_EVA"

    choices = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (ADMIN_EVA, 'Администратор ЕВА'),
    )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя. Заменяет стандартного пользователя Django
    """

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    username = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        unique=True,
    )
    first_name = models.CharField(
        max_length=75,
        verbose_name='Имя сотрудника',
        help_text='Введите имя сотрудника',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия сотрудника',
        help_text='Введите фамилию сторудника',
    )
    patronymic = models.CharField(
        verbose_name="Отчество",
        help_text="Введите отчество (при наличии)",
        max_length=30,
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name="Роль пользователя",
        help_text="Выберите роль пользователя",
    )
    phone_number = PhoneNumberField(
        verbose_name='Рабочий телефон',
        help_text="Введите рабочий телефон сотрудника",
        default='+78122468400'
    )
    email = models.EmailField(
        blank=True,
    )
    tools = models.ManyToManyField(to=Tools,
                                   related_name='tools',
                                   blank=True,
                                   verbose_name='Инструменты', )

    is_active = models.BooleanField(
        verbose_name="Аккаунт активен?",
        help_text="Укажите, активен ли аккаунт",
        blank=True,
    )

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_eva_admin(self):
        return self.role == UserRoles.ADMIN_EVA

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
