from django.db import models

from portal.models import Tools


class PanelTool(Tools):

    class Meta:
        verbose_name = 'Система контроля отправки ИС ИАО'
        verbose_name_plural = 'Системы контроля отправки ИС ИАО'

    def __str__(self):
        return self.full_name


class ResultTask(models.Model):

    class Status(models.TextChoices):
        success = 'SUCCESS', 'SUCCESS'
        fail = 'FAIL', 'FAIL'
        error = 'ERROR', 'ERROR'

    class Periodic(models.TextChoices):
        day = 'Day', 'Day'
        week = 'Week', 'Week'
        month = 'Month', 'Month'
        quarter = 'Quarter', 'Quarter'
        half_year = 'Half-year', 'Half-year'
        year = 'Year', 'Year'

    datetime = models.DateTimeField(
        verbose_name='Дата и время выполнения задачи.',
        auto_now_add=True
    )
    periodicity = models.CharField(
        verbose_name='Периодичность выполения задачи',
        help_text='Выберите периодичность выполения.',
        max_length=10,
        choices=Periodic.choices,
        default=Periodic.day,
    )
    status = models.CharField(
        verbose_name='Статус выполнения.',
        help_text='Выберите статус выполнения.',
        max_length=8,
        choices=Status.choices,
        default=Status.success,
    )
    full_name = models.CharField(
        verbose_name='Название задачи.',
        max_length=255
    )
    body = models.TextField(
        verbose_name='Данные из автоматической отправки данных.',
        help_text='Данные из задачи. В случае удачи requestId и datasets, иначе response.text'
    )

    def __str__(self):
        return f'{self.datetime} - {self.periodicity} - {self.status}'

    class Meta:
        verbose_name = 'Результат выполнения отправки данных в ИС ИАО'
        verbose_name_plural = 'Результаты выполнения отправки данных в ИС ИАО'
