from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from redis.exceptions import ConnectionError as DoesNotConnectRedis
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from eva.reports.models import Reports
from eva.reports.serializers import ReportsListSerializer
from eva.reports.utils import (convert_data_to_docs_format,
                               create_report_key_in_redis_db,
                               generate_content_type_for_download,
                               get_data_from_redis)


def download_report_file(requests, report_number: str, file_extension: str):
    report = Reports.objects.get(serial_number=float(report_number))
    response = HttpResponse(
        content_type=generate_content_type_for_download(type_of_header=file_extension),
    )
    response['Content-Disposition'] = f'attachment; filename={report.serial_number}.{file_extension}'
    try:
        data = get_data_from_redis(report_number)
        convert_data_to_docs_format(response=response, file_extension=file_extension, redis_data=data)
        return response
    except TypeError:
        return JsonResponse({'detail': 'Необходимо повторно сгенерировать отчет'}, status=404)


class ReportView(APIView):
    def get(self, request, report_serial_number: str, data_format=None):
        try:
            report = Reports.objects.get(serial_number=float(report_serial_number))
            if data_format == 'csv':
                return redirect('download', report_number=report_serial_number, file_extension='csv')
            if data_format == 'json':
                return JsonResponse(get_data_from_redis(report_serial_number), status=200)
            if data_format == 'xlsx':
                return redirect('download', report_number=report_serial_number, file_extension='xlsx')
            create_report_key_in_redis_db(report=report)
            return JsonResponse({'details': 'Ключ записан в редис'}, status=200)
        except TypeError:
            return JsonResponse({'details': 'Ключ в редис не найден'}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({'detail': 'Отчета с таким номером не существует'}, status=404)
        except DoesNotConnectRedis:
            return JsonResponse({
                'detail': 'Не могу подключиться к redis. '
                          'Сообщите администратору системы или в отдел сопровождения СПО'},
                status=502)


class ReportsListView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsListSerializer
