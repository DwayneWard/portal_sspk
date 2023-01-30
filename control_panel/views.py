from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView, ListAPIView

from control_panel.models import TaskResult
from control_panel.serializers import TaskResultSerializer


class TasksResultsView(ListAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
