from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authority.models import User
from portal.models import Tools
from portal.serializers import ToolsSerializer


class UsersSerializer(serializers.ModelSerializer):
    tools = ToolsSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'groups', 'user_permissions')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserChangeSerializer(serializers.ModelSerializer):
    tools = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Tools.objects.all(),
        slug_field='full_name',
    )

    class Meta:
        model = User
        exclude = ('password', 'last_login',)
