from django.urls import path

from app_api.views import DirectionListAPIView, DisciplineListAPIView, \
    StudentListAPIView

urlpatterns = [
    path('directions/', DirectionListAPIView.as_view(), name='directions'),
    path('disciplines/', DisciplineListAPIView.as_view(), name='disciplines'),
    path('students/', StudentListAPIView.as_view(), name='students')
]
