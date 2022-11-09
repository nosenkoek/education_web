from django.http import HttpResponse
from rest_framework.views import APIView

from app_education.models import Direction
from app_report.services.report_handler import ReportHandler


class ReportView(APIView):
    """View для получения отчета"""
    def get(self, request):
        directions = Direction.objects\
            .prefetch_related('discipline',
                              'class_set__student_set') \
            .select_related('curator_fk').all()
        ReportHandler(directions).create_report()
        return HttpResponse('OK')
