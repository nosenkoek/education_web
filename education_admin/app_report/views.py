from uuid import uuid4

from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView

from app_report.services.looking_for_files import get_path_file
from app_report.tasks import create_report
from celery.result import AsyncResult


class ReportView(APIView):
    """View для получения отчета"""
    def get(self, request):
        task_id = str(uuid4())
        result = create_report.apply_async((task_id, ), task_id=task_id)
        return HttpResponse(f'Ваш отчет № {result.task_id}')


class StatusReportView(APIView):
    """View для получения результата о статусе"""
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        res = AsyncResult(task_id)
        if res.ready():
            messages = f'Отчет № {task_id} ГОТОВ. ' \
                       'Можно скачать по ссылке:' \
                       f'<a href="/report/download/{task_id}">Скачать</a>'
        else:
            messages = f'Отчет № {task_id} в процессе создания. '

        return HttpResponse(messages)


class DownloadReportView(APIView):
    """View для загрузки файла"""
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        file_name = f'report_{task_id}.xlsx'
        result = get_path_file(file_name)
        if result:
            return FileResponse(open(result, 'rb'))
        return HttpResponse('Файл не найден')
