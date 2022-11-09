from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from app_education.models import Direction
from app_students.services.increment_utils import get_next_increment


MAX_STUDENT_IN_CLASS = 20


class Class(models.Model):
    """Студенческая группа"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    number = models.IntegerField(unique=True,
                                 default=get_next_increment,
                                 editable=False,
                                 verbose_name=_('number'))
    direction_fk = models.ForeignKey(Direction,
                                     on_delete=models.CASCADE,
                                     to_field='id',
                                     db_column='direction_fk',
                                     verbose_name=_('direction'))

    class Meta:
        managed = False
        db_table = 'class'
        verbose_name = _('class')
        verbose_name_plural = _('classes')

    def __str__(self):
        return _('Group №{}').format(self.number)

    def free_place(self):
        """
        Подсчет количества свободных мест в группе.
        :return:
        """
        count_students = self.student_set.count()
        return MAX_STUDENT_IN_CLASS - count_students

    def count_female(self):
        return self.student_set.filter(gender='female').count()

    def count_male(self) -> int:
        return self.student_set.filter(gender='male').count()


class Student(models.Model):
    """Студенты"""
    class TypeGender(models.TextChoices):
        FEMALE = 'female', _('female')
        MALE = 'male', _('male')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    first_name = models.CharField(max_length=30, verbose_name=_('first name'))
    last_name = models.CharField(max_length=30, verbose_name=_('last name'))
    patronymic = models.CharField(max_length=30, verbose_name=_('patronymic'),
                                  null=True, blank=True)
    email = models.CharField(unique=True, max_length=30,
                             verbose_name='email')
    tel_number = models.CharField(unique=True, max_length=30,
                                  verbose_name=_('telephone number'))
    gender = models.CharField(max_length=10, choices=TypeGender.choices,
                              verbose_name=_('gender'))

    direction_fk = models.ForeignKey(Direction,
                                     on_delete=models.CASCADE,
                                     to_field='id',
                                     db_column='direction_fk',
                                     verbose_name=_('direction'))

    class_fk = models.ForeignKey(Class,
                                 null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 to_field='id',
                                 db_column='class_fk',
                                 verbose_name=_('class'))

    class Meta:
        managed = False
        db_table = 'student'
        verbose_name = _('student')
        verbose_name_plural = _('students')

    def get_full_name(self):
        if self.patronymic is None:
            return f'{self.last_name} {self.first_name}'
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def __str__(self):
        return self.get_full_name()
