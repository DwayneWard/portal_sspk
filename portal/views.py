from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from portal.models import Tools
from portal.serializers import ToolsSerializer


class ToolsForCurrentUser(GenericAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_tools = list(map(lambda tool: ToolsSerializer(tool).data, current_user.tools.all()))

        return JsonResponse(user_tools, safe=False)
