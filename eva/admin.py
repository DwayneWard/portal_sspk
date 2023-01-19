from django.contrib import admin

from eva.models import EvaTool
from eva.ISIAO.models import GIS, Indicator
from eva.Reports.models import Reports, Category

admin.site.register(EvaTool)
admin.site.register(Reports)
admin.site.register(GIS)
admin.site.register(Indicator)
admin.site.register(Reports)
admin.site.register(Category)