from django.db import models

from authority.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=100,
        unique=True
    )
    serial_number = models.PositiveIntegerField(
        verbose_name='Порядковый номер категории',
        primary_key=True,
    )

    def __str__(self):
        return f'{self.serial_number} - {self.name}'

    class Meta:
        verbose_name = 'Категория отчета'
        verbose_name_plural = 'Категории отчетов'


class Reports(models.Model):
    name = models.CharField(
        verbose_name='Наименование отчета',
        max_length=100,
        unique=True
    )
    serial_number = models.FloatField(
        verbose_name='Порядковый номер отчета',
        primary_key=True,
    )
    zammad_queryset = models.TextField(
        verbose_name='SQL запрос к Zammad БД'
    )
    users = models.ManyToManyField(
        User,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Категория отчета',
        default=1,
    )

    def __str__(self):
        return f'{self.serial_number} - {self.name}'

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
