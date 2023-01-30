from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from authority.models import User
from authority.serializers import UserCreateSerializer, UsersSerializer, UserChangeSerializer


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangeSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

