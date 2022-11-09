from celery import shared_task
from app_education.models import Direction
from app_report.services.report_handler import ReportHandler


@shared_task
def create_report(task_id):
    directions = Direction.objects \
        .prefetch_related('discipline',
                          'class_set__student_set') \
        .select_related('curator_fk').all()

    ReportHandler(directions).create_report(task_id)
