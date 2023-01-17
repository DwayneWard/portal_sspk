from portal.models import Tools


class EvaTool(Tools):
    class Meta:
        verbose_name = "Инструмент EVA"
        verbose_name_plural = "Инструменты EVA"

    def __str__(self):
        return self.full_name
