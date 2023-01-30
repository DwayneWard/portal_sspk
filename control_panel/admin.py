from django.contrib import admin

from control_panel.models import TaskResult


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'color',)
    search_fields = ('color',)
    list_filter = ('color', 'date',)
