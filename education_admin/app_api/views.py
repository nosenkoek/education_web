from rest_framework.generics import ListAPIView

from app_api.serializers import DirectionSerializer, DisciplineSerializer, \
    StudentSerializer
from app_education.models import Direction, Discipline
from app_students.models import Student


class DirectionList(ListAPIView):
    """Контроллер для списка направлений"""
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class DisciplineListAPIView(ListAPIView):
    """Контроллер для списка дисциплин"""
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

    def get_queryset(self):
        """
        Возвращает QuerySet с фильтрацией по направлению.
        :return: queryset со всеми объектами или отфильтрованные
        по названию или id направления
        """
        queryset = super(DisciplineListAPIView, self).get_queryset()
        direction_name = self.request.query_params.get('direction_name')
        direction_id = self.request.query_params.get('direction_id')

        if direction_name:
            queryset = queryset.filter(
                direction__name__icontains=direction_name)
        elif direction_id:
            queryset = queryset.filter(direction__id=direction_id)
        else:
            queryset = queryset.all()
        return queryset


class StudentListAPIView(ListAPIView):
    """Контроллер для списка студентов"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        Возвращает QuerySet с фильтрацией по направлению.
        :return: queryset со всеми объектами или отфильтрованные
        по названию или id направления
        """
        queryset = super(StudentListAPIView, self).get_queryset()
        last_name = self.request.query_params.get('last_name')
        direction_id = self.request.query_params.get('direction_id')
        class_id = self.request.query_params.get('class_id')

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        if direction_id:
            queryset = queryset.filter(direction_fk__id=direction_id)
        elif class_id:
            queryset = queryset.filter(class_fk__id=class_id)
        else:
            queryset = queryset.all()
        return queryset
