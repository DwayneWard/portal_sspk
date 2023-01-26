from rest_framework import serializers

from portal.models import Tools


class ToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = ('full_name', 'logo_pic', 'main_url')
