from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from authority.models import User
from authority.permisions import IsAdminOrAdminEVA
from authority.serializers import (CustomTokenObtainPairSerializer, UserChangeSerializer, UserCreateSerializer,
                                   UsersSerializer)


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class UserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangeSerializer
    permission_classes = [IsAdminOrAdminEVA,]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CabinetView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def get(self, request, *args, **kwargs):
        current_user = request.user

        return JsonResponse(data=UsersSerializer(current_user).data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
