from uuid import uuid4

from django.http import HttpResponse, FileResponse
from django.urls import reverse
from django.views import View

from app_report.services.looking_for_files import get_path_file
from app_report.tasks import create_report
from celery.result import AsyncResult


class ReportView(View):
    """View для получения отчета"""
    def get(self, request):
        task_id = str(uuid4())
        result = create_report.apply_async((task_id, ), task_id=task_id)
        url_address = reverse('status', kwargs={'task_id': task_id})
        return HttpResponse(f'Ваш отчет № {result.task_id}<br>'
                            f'Узнать статус можно по ссылке:'
                            f'<a href="{url_address}">Статус</a>')


class StatusReportView(View):
    """View для получения результата о статусе"""
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        res = AsyncResult(task_id)
        if res.ready():
            url_address = reverse('download', kwargs={'task_id': task_id})
            messages = f'Отчет № {task_id} ГОТОВ.<br> ' \
                       'Можно скачать по ссылке:' \
                       f'<a href="{url_address}">Скачать</a>'
        else:
            messages = f'Отчет № {task_id} в процессе создания. '

        return HttpResponse(messages)


class DownloadReportView(View):
    """View для загрузки файла"""
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        file_name = f'report_{task_id}.xlsx'
        result = get_path_file(file_name)
        if result:
            return FileResponse(open(result, 'rb'))
        return HttpResponse('Файл не найден')
