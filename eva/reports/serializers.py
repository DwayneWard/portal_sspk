from rest_framework import serializers

from eva.reports.models import Category, Reports


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'serial_number',
                  'name',
                  ]


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ('serial_number', 'name')
