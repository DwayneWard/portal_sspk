from _ast import Is

from django.db.models import Q
from psycopg2.errors import SyntaxError as SQLSyntaxError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from redis.exceptions import ConnectionError as DoesNotConnectRedis
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from eva.reports.models import Reports, Category
from eva.reports.serializers import ReportsSerializer
from eva.reports.utils import (convert_data_to_docs_format,
                               create_report_key_in_redis_db,
                               generate_content_type_for_download,
                               get_data_from_redis)


def download_report_file(requests, report_serial_number: str, file_extension: str):
    report = Reports.objects.get(serial_number=float(report_serial_number))
    response = HttpResponse(
        content_type=generate_content_type_for_download(type_of_header=file_extension),
    )
    response['Content-Disposition'] = f'attachment; filename={report.serial_number}.{file_extension}'
    try:
        data = get_data_from_redis(report_serial_number)
        convert_data_to_docs_format(response=response, file_extension=file_extension, redis_data=data)
        return response
    except TypeError:
        return JsonResponse({'detail': 'Необходимо повторно сгенерировать отчет'}, status=404)


class GenerateReportView(APIView):
    def get(self, request, report_serial_number: str):
        try:
            report = Reports.objects.get(serial_number=float(report_serial_number))
            create_report_key_in_redis_db(report=report)
            return JsonResponse({'details': 'Ключ записан в редис'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'detail': 'Отчета с таким номером не существует'}, status=404)
        except DoesNotConnectRedis:
            return JsonResponse({
                'detail': 'Не могу подключиться к redis. '
                          'Сообщите администратору системы или в отдел сопровождения СПО'},
                status=502)
        except SQLSyntaxError:
            return JsonResponse({'detail': 'Ошибка в запросе на получение отчета. Обратитесь к администратору.'},
                                status=404)


class ReportAtJsonFormatView(APIView):
    def get(self, request, report_serial_number: str):
        try:
            return JsonResponse(get_data_from_redis(report_serial_number), status=200)
        except TypeError:
            return JsonResponse({'details': 'Ключ в редис не найден'}, status=404)


class CategoriesWithReportsView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        current_user = request.user

        reports = Reports.objects.filter(users=current_user).prefetch_related('category')

        data = {}
        for report in reports:
            data.setdefault(report.category.name, []).append(ReportsSerializer(report).data)

        return JsonResponse(data, status=200)
