from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from authority.permisions import IsAdminOrAdminEVA
from eva.isiao.models import GIS, Indicator
from eva.isiao.serializers import GISSerializer, IndicatorSerializer


class IndicatorsListView(ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class IndicatorCreateView(CreateAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class IndicatorView(RetrieveUpdateDestroyAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class GISListView(ListAPIView):
    queryset = GIS.objects.all()
    serializer_class = GISSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class GISCreateView(CreateAPIView):
    queryset = GIS.objects.all()
    serializer_class = GISSerializer
    permission_classes = [IsAdminOrAdminEVA,]


class GISView(RetrieveUpdateDestroyAPIView):
    queryset = GIS.objects.all()
    serializer_class = GISSerializer
    permission_classes = [IsAdminOrAdminEVA,]
