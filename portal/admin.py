from django.contrib import admin

from portal.models import Tools


@admin.register(Tools)
class ToolsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'main_url',)
    search_fields = ('full_name',)
