from django.contrib import admin

from eva.models import EvaTool
from eva.isiao.models import GIS, Indicator
from eva.reports.models import Reports, Category

admin.site.register(EvaTool)
admin.site.register(Reports)
admin.site.register(GIS)
admin.site.register(Indicator)
admin.site.register(Category)