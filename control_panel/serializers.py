from rest_framework import serializers

from control_panel.models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    color = serializers.CharField(max_length=50)

    class Meta:
        model = TaskResult
        fields = ('date', 'status', 'full_name', 'periodicity', 'color',)
