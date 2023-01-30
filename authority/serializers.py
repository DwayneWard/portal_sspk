from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from authority.models import User
from portal.models import Tools
from portal.serializers import ToolsSerializer


class UsersSerializer(serializers.ModelSerializer):
    tools = ToolsSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    tools = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Tools.objects.all(),
        slug_field='tools',
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            'tools',
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login',)
