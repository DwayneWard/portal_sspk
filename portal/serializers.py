from rest_framework import serializers

from portal.models import Tools


class ToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        exclude = ('id', 'polymorphic_ctype',)
