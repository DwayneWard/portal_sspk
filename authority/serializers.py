from rest_framework import serializers

from authority.models import User
from portal.models import Tools
from portal.serializers import ToolsSerializer


class UsersSerializer(serializers.ModelSerializer):
    tools = ToolsSerializer(many=True)

    class Meta:
        model = User
        exclude = ('is_staff', 'groups', 'user_permissions')


class UserCreateSerializer(serializers.ModelSerializer):
    tools = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Tools.objects.all(),
        slug_field='tool',
    )

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
