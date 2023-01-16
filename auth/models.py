from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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
    # TODO: Добавить связь пользователь - инструменты, когда появится приложуха с инструментами

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
