from portal.models import Tools


class PanelTool(Tools):

    class Meta:
        verbose_name = 'Система контроля отправки ИС ИАО'
        verbose_name_plural = 'Системы контроля отправки ИС ИАО'

    def __str__(self):
        return self.full_name
