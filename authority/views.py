from rest_framework.generics import ListAPIView

from authority.models import User
from authority.serializers import UsersSerializer


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
