import json

from django.http import HttpResponse, JsonResponse
from redis.client import StrictRedis
from rest_framework.views import APIView

from eva.Reports.models import Reports
from eva.Reports.utils import (convert_data_to_docs_format,
                               generate_content_type_for_download)


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
    pass