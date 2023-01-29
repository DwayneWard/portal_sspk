from rest_framework.generics import CreateAPIView, ListAPIView

from authority.models import User
from authority.serializers import UserCreateSerializer, UsersSerializer


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
