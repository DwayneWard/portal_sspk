from rest_framework import serializers

from eva.isiao.models import GIS, Indicator


class GISSerializer(serializers.ModelSerializer):
    class Meta:
        model = GIS
        fields = '__all__'


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'
