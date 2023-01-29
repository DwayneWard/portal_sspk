from rest_framework import serializers

from control_panel.models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('date', 'color', 'full_name', 'periodicity',)
