from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from eva.isiao.models import Indicator, GIS
from eva.isiao.serializers import IndicatorSerializer, GISSerializer


class IndicatorsListView(ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class IndicatorCreateView(CreateAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class IndicatorView(RetrieveUpdateDestroyAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class GISListView(ListAPIView):
    queryset = GIS.objects.all()
    serializer_class = GISSerializer


class GISCreateView(CreateAPIView):
    queryset = GIS.objects.all()
    serializer_class = GISSerializer


class GISView(RetrieveUpdateDestroyAPIView):
    queryset = GIS.objects.all()
    serializer_class = GISSerializer
