from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView, GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authority.models import User
from authority.serializers import (UserChangeSerializer, UserCreateSerializer,
                                   UsersSerializer)


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangeSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CabinetView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        current_user = request.user

        return JsonResponse(data=UsersSerializer(current_user).data, status=status.HTTP_200_OK)
