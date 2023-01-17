from django.db import models


class GIS(models.Model):

    full_name = models.CharField(
        max_length=1000,
        verbose_name='Название ГИС',
        help_text='Введите название ГИС без сокращения, например, '
                  'Единая система строительного комплекса Санкт-Петербурга',
    )
    short_name = models.CharField(
        max_length=50,
        verbose_name='Аббревиатура ГИС',
        help_text='Аббревиатура ГИС',
    )
    dashboard_code = models.CharField(
        max_length=50,
        verbose_name='Код системы в ИС ИАО',
        blank=True,
        null=True
    )
    zammad_systemcode = models.IntegerField(
        verbose_name='ИД системы в Zammad',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.short_name

    class Meta:
        verbose_name = 'ГИС'
        verbose_name_plural = 'ГИСЫ'


class Indicator(models.Model):

    choices = (
        ('day', 'день'),
        ('month', 'месяц')
    )
    full_name = models.TextField(
        verbose_name='Полное наименование показателя',
        max_length=250
    )
    ias_code = models.CharField(
        verbose_name='Код показателя',
        max_length=15
    )
    periodicity = models.CharField(
        verbose_name='Периодичность обновления показателя',
        choices=choices,
        default='day',
        max_length=10
    )
    zammad_queryset = models.TextField(
        verbose_name='SQL запрос к Zammad БД'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Показатель ИС ИАО'
        verbose_name_plural = 'Показатели ИС ИАО'
