from django.contrib import admin

from control_panel.models import TaskResult


@admin.register(TaskResult)
class ResultTaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'status',)
    search_fields = ('status',)
    list_filter = ('status', 'date',)
