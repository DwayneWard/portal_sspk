from django.db import models
from polymorphic.models import PolymorphicModel


class Tools(PolymorphicModel):
    """
    Абстрактная модель для инструментов, которая обьединяет общую информацию инструментов.
    Наследоваться от нее при создании новых инструментов.
    """
    full_name = models.CharField(
        verbose_name='Полное имя инструмента',
        max_length=250,
        unique=True
    )
    logo_pic = models.ImageField(
        verbose_name='Логотип инструмента.',
        upload_to='tools_logo/'
    )
    main_url = models.URLField(
        verbose_name='URL ведущий на главную страницу инструмента'
    )

    class Meta:
        verbose_name = "Инструмент Портала"
        verbose_name_plural = "Инструменты Портала"

    def __str__(self):
        return self.full_name
