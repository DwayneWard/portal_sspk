from django.db import models


class Tools(models.Model):

    '''
        Абстрактная модель для инструментов, которая обьединяет общую информацию инструментов.
    '''

    full_name = models.CharField(
        verbose_name='Полное имя инструмента',
        max_length=250,
        unique=True
    )
    logo_pic = models.ImageField(
        verbose_name='Логотип инструмента.',
        upload_to='control_panel/tools_logo/'
    )
    main_url = models.URLField(
        verbose_name='URL ведущий на главную страницу инструмента.'
    )

    class Meta:
        abstract = True
