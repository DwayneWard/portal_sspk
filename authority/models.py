from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from portal.models import Tools


class User(AbstractUser):
    """
    Модель пользователя. Заменяет стандартного пользователя Django
    """
    phone_number = PhoneNumberField(
        verbose_name='Рабочий телефон',
        help_text="Введите рабочий телефон сотрудника",
        default='+78122468400'
    )
    patronymic = models.CharField(
        verbose_name="Отчество",
        help_text="Введите отчество (при наличии)",
        max_length=30,
        null=True,
        blank=True,
    )
    tools = models.ManyToManyField(to=Tools,
                                   related_name='tools',
                                   blank=True,
                                   verbose_name='Инструменты', )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"