from rest_framework import serializers

from eva.reports.models import Category, Reports


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('serial_number', 'name',)


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ('serial_number', 'name')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'
