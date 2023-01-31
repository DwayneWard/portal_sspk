from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from control_panel.models import TaskResult
from control_panel.serializers import TaskResultSerializer
from eva.isiao.tasks import (send_data_to_ias_everyday,
                             send_data_to_ias_everyweek,
                             send_data_to_ias_periodic)


class TasksResultsView(ListAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer


@api_view(['GET', ])
def resend_tasks(request):
    if request.method == 'GET':
        bad_tasks = TaskResult.objects.filter(color__in=('red', 'yellow'))
        for task in bad_tasks:
            if task.periodicity == 'day':
                date = task.date
                send_data_to_ias_everyday.apply_async(args=[date, ])
            elif task.periodicity == 'week':
                send_data_to_ias_everyweek.apply_async(args=[task.date, ])
            else:
                send_data_to_ias_periodic.apply_async(args=[task.date, ])
        return JsonResponse({'detail': 'Неудачно выполненные задачи успешно переотправлены'})
