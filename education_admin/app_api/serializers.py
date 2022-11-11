from rest_framework import serializers

from app_education.models import Direction, Discipline
from app_students.models import Student


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    direction_name = serializers.CharField(source='direction_fk.name')

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'patronymic',
                  'email', 'tel_number', 'gender', 'direction_fk',
                  'direction_name', 'class_fk')
