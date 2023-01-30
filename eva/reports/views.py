from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from redis.exceptions import ConnectionError as DoesNotConnectRedis
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from eva.reports.models import Reports
from eva.reports.serializers import ReportSerializer, ReportsSerializer
from eva.reports.utils import (convert_data_to_docs_format,
                               create_report_key_in_redis_db,
                               generate_content_type_for_download,
                               get_data_from_redis)


class DownloadFilesView(GenericAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get(self, request, *args, **kwargs):
        report = Reports.objects.get(serial_number=float(self.kwargs['pk']))
        file_extension = kwargs.get('file_extension')
        response = HttpResponse(
            content_type=generate_content_type_for_download(type_of_header=file_extension),
        )
        response['Content-Disposition'] = f'attachment; filename={report.serial_number}.{file_extension}'
        try:
            data = get_data_from_redis(self.kwargs['pk'])
            convert_data_to_docs_format(response=response, file_extension=file_extension, redis_data=data)
            return response
        except TypeError:
            return JsonResponse({'detail': 'Необходимо повторно сгенерировать отчет'}, status=404)


class ReportAtJsonFormatView(GenericAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse(get_data_from_redis(self.kwargs['pk']), status=200)
        except TypeError:
            return JsonResponse({'details': 'Ключ в редис не найден'}, status=404)


class CategoriesWithReportsView(GenericAPIView):
    queryset = Reports.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportsSerializer

    def get(self, request, *args, **kwargs):
        current_user = request.user

        reports = Reports.objects.filter(users=current_user).prefetch_related('category')

        data = {}
        for report in reports:
            data.setdefault(report.category.name, []).append(ReportsSerializer(report).data)

        return JsonResponse(data, status=200)


class ReportCreateView(CreateAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer


class ReportView(RetrieveUpdateDestroyAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer

    def get(self, request, *args, **kwargs):
        try:
            report = Reports.objects.get(serial_number=float(self.kwargs['pk']))
            create_report_key_in_redis_db(report=report)
            return JsonResponse({'details': 'Ключ записан в редис'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'detail': 'Отчета с таким номером не существует'}, status=404)
        except DoesNotConnectRedis:
            return JsonResponse({
                'detail': 'Не могу подключиться к redis. '
                          'Сообщите администратору системы или в отдел сопровождения СПО'},
                status=502)
        except SyntaxError:
            return JsonResponse({'detail': 'Ошибка в запросе на получение отчета. Обратитесь к администратору.'},
                                status=404)
