from django.urls import path

from app_api.views import DirectionList, DisciplineList, StudentList

urlpatterns = [
    path('directions/', DirectionList.as_view(), name='directions'),
    path('disciplines/', DisciplineList.as_view(), name='disciplines'),
    path('students/', StudentList.as_view(), name='students')
]
