from django.urls import path

from app_report.views import ReportView, StatusReportView, DownloadReportView

urlpatterns = [
    path('', ReportView.as_view(), name='report'),
    path('status/<str:task_id>', StatusReportView.as_view(), name='status'),
    path('download/<str:task_id>', DownloadReportView.as_view(),
         name='download')
]
