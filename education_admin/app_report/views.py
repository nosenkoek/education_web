import logging
from uuid import uuid4

from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.http import HttpResponse, FileResponse
from django.urls import reverse
from django.views.generic import View
from django.utils.translation import gettext as _

from app_report.services.looking_for_files import get_path_file
from app_report.tasks import create_report
from celery.result import AsyncResult

logger = logging.getLogger(__name__)


class AdminPermissionRequiredMixin(PermissionRequiredMixin,
                                   LoginRequiredMixin):
    login_url = '/admin/'
    permission_denied_message = _("You don't have permission. "
                                  "It can do only admin")
    permission_required = 'app_education.view_direction'


class ReportView(AdminPermissionRequiredMixin, View):
    """View для получения отчета"""
    def get(self, request):
        task_id = str(uuid4())
        result = create_report.apply_async((task_id, ), task_id=task_id)
        logger.info(f'Create task report {task_id}')
        url_address = reverse('status', kwargs={'task_id': task_id})
        return HttpResponse(f'Ваш отчет № {result.task_id}<br>'
                            f'Узнать статус можно по ссылке:'
                            f'<a href="{url_address}">Статус</a>')


class StatusReportView(AdminPermissionRequiredMixin, View):
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


class DownloadReportView(AdminPermissionRequiredMixin, View):
    """View для загрузки файла"""
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        file_name = f'report_{task_id}.xlsx'
        result = get_path_file(file_name)
        if result:
            logger.info(f'Download task report {task_id}')
            return FileResponse(open(result, 'rb'))
        return HttpResponse('Файл не найден')
