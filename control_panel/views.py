from rest_framework import response
from rest_framework.generics import ListAPIView

from control_panel.models import TaskResult
from control_panel.serializers import TaskResultSerializer
from eva.isiao.tasks import (send_data_to_ias_everyday,
                             send_data_to_ias_everyweek,
                             send_data_to_ias_periodic)


class TasksResultsView(ListAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer


class ResendTaskResultView(ListAPIView):

    def get(self, request, *args, **kwargs):
        queryset = TaskResult.objects.filter(color__in=('red', 'yellow'))
        for task in queryset:
            if task.periodicity == 'day':
                send_data_to_ias_everyday.apply_async(args=[task.date, ])
            elif task.periodicity == 'week':
                send_data_to_ias_everyweek.apply_async(args=[task.date, ])
            else:
                send_data_to_ias_periodic.apply_async(args=[task.date, ])
        serializer = TaskResultSerializer(queryset, many=True)
        return response.Response(serializer.data)
