import json

from django.http import HttpResponse, JsonResponse
from redis.client import StrictRedis
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from eva.isiao.utils import get_connect_with_redis
from eva.reports.models import Reports
from eva.reports.serializers import ReportsListSerializer
from eva.reports.utils import (convert_data_to_docs_format,
                               generate_content_type_for_download, create_report_key_in_redis_db)


def download_report_file(requests, report_number: int, redis_db: StrictRedis, file_extension: str):
    try:
        report = Reports.objects.get(serial_number=report_number)
        response = HttpResponse(
            content_type=generate_content_type_for_download(type_of_header=file_extension),
        )
        response['Content-Disposition'] = f'attachment; filename={report.serial_number}.{file_extension}'
        try:
            data = json.loads(redis_db.get(str(report.serial_number)))
            convert_data_to_docs_format(response=response, file_extension=file_extension, redis_data=data)
            return response
        except Exception as e:
            return JsonResponse({'Error': f'{e}', 'detail': 'Необходимо повторно сгенерировать отчет'})
    except Exception as e:
        return JsonResponse({'Error': f'{e}', 'detail': 'Отчета с таким номером не существует'})


class ReportView(APIView):
    def get(self, request, report_serial_number, data_format=None):
        report = Reports.objects.filter(serial_number=float(report_serial_number)).first()
        if data_format == 'csv':
            pass
        if data_format == 'json':
            pass
        if data_format == 'xlsx':
            pass
        create_report_key_in_redis_db(redis_db=get_connect_with_redis(), report=report)
        return JsonResponse({'details': 'Ключ записан в редис'})


class ReportsListView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsListSerializer
