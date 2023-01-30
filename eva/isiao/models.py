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

    def generate_series(self, value: int, times: str) -> dict:
        """
        Метод модели для генерации серии в структуре необходимой для передачи в ИС ИАО.


        :param value: Численный показатель по данному ГИСу по показателю ИС ИАО (Indicator) на основе zammad_queryset.
        :param times: Показатель времени за какой промежуток генерируется серия день/неделя/месяц/квартал/полугодие/год.
        :return: Возвращает серию в формате словаря, которая будет использоваться в формировании dataset'а в
        generate_data.
        """
        series = {
            "dimensions": [
                {
                    "ref": "territory",
                    "value": "40000000000"
                },
                {
                    "ref": "System",
                    "value": self.dashboard_code
                }
            ],
            "attributes": [
                {
                    "ref": "unit",
                    "value": "ед."
                }
            ],
            "observation": {
                "time": times,
                "value": value
            }
        }
        return series


class Indicator(models.Model):

    choices = (
        ('day', 'День'),
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('quarter', 'Квартал'),
        ('half-year', 'Полгода'),
        ('year', 'Год'),
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
