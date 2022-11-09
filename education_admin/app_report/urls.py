from django.urls import path

from app_report.views import ReportView

urlpatterns = [
    path('', ReportView.as_view(), name='report')
]
