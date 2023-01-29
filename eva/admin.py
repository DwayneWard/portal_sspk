from django.contrib import admin

from eva.isiao.models import GIS, Indicator
from eva.reports.models import Category, Reports


@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'category',)
    search_fields = ('serial_number', 'name', 'users',)
    list_filter = ('serial_number',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name',)
    search_fields = ('serial_number', 'name',)
    list_filter = ('serial_number',)


@admin.register(GIS)
class GISAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'dashboard_code', 'zammad_systemcode',)
    search_fields = ('short_name', 'dashboard_code',)


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'periodicity', 'ias_code',)
    search_fields = ('ias_code',)
    list_filter = ('periodicity', 'ias_code')
