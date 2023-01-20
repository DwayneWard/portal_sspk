from rest_framework import serializers

from eva.reports.models import Category, Reports


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'serial_number',
                  'name',
                  ]


class ReportsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Reports
        fields = ['id',
                  'serial_number',
                  'users',
                  'category',
                  ]
