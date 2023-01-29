from django.db import models

from portal.models import Tools


class PanelTool(Tools):
    class Meta:
        verbose_name = 'Система контроля отправки ИС ИАО'
        verbose_name_plural = 'Системы контроля отправки ИС ИАО'

    def __str__(self):
        return self.full_name


class TaskResult(models.Model):
    class Colors(models.TextChoices):
        red = 'red', 'Красный'
        yellow = 'yellow', 'Желтый'
        green = 'green', 'Зеленый'

    class Periodic(models.TextChoices):
        day = 'day', 'День'
        week = 'week', 'Неделя'
        month = 'month', 'Месяц'
        quarter = 'quarter', 'Квартал'
        half_year = 'half-year', 'Полгода'
        year = 'year', 'Год'

    date = models.DateField(
        verbose_name='Дата выполнения задачи',
    )
    periodicity = models.CharField(
        verbose_name='Периодичность выполения задачи',
        help_text='Выберите периодичность выполения',
        max_length=10,
        choices=Periodic.choices,
        default=Periodic.day,
    )
    color = models.CharField(
        verbose_name='Статус выполнения',
        help_text='Выберите статус выполнения',
        max_length=7,
        choices=Colors.choices,
        default=Colors.green,
    )
    full_name = models.CharField(
        verbose_name='Название задачи',
        max_length=255
    )
    # TODO: подумать, может это поле не надо
    body = models.TextField(
        verbose_name='Данные из автоматической отправки данных',
        help_text='Данные из задачи. В случае удачи requestId и datasets, иначе response.text'
    )

    def __str__(self):
        return f'{self.date} - {self.periodicity} - {self.status}'

    class Meta:
        verbose_name = 'Результат выполнения отправки данных в ИС ИАО'
        verbose_name_plural = 'Результаты выполнения отправки данных в ИС ИАО'
        constraints = [
            models.UniqueConstraint(fields=['date', 'periodicity'], name='date and periodicity'),
        ]
