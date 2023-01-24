from django.contrib import admin

from eva.isiao.models import GIS, Indicator
from eva.models import EvaTool
from eva.reports.models import Category, Reports

admin.site.register(EvaTool)
admin.site.register(Reports)
admin.site.register(GIS)
admin.site.register(Indicator)
admin.site.register(Category)
