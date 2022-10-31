from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Discipline(models.Model):
    """Учебная дисциплина (предмет)"""
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'discipline'
        verbose_name = _('discipline')
        verbose_name_plural = _('disciplines')

    def __str__(self):
        return self.name


class Direction(models.Model):
    """Направление подготовки"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))

    # TODO: продумать как ограничить куратор/админ
    curator_fk = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   to_field='id',
                                   db_column='curator_fk',
                                   verbose_name=_('curator'))

    discipline = models.ManyToManyField(Discipline,
                                        through='DirectionDiscipline')

    class Meta:
        managed = False
        db_table = 'direction'
        verbose_name = _('direction of education')
        verbose_name_plural = _('directions of education')

    def __str__(self):
        return self.name


class DirectionDiscipline(models.Model):
    """Таблица связи между дисциплинами и направлениями подготовки"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    direction_fk = models.ForeignKey(Direction,
                                     on_delete=models.CASCADE,
                                     to_field='id',
                                     db_column='direction_fk',
                                     verbose_name=_('direction of education'))
    discipline_fk = models.ForeignKey(Discipline,
                                      on_delete=models.CASCADE,
                                      to_field='id',
                                      db_column='discipline_fk',
                                      verbose_name=_('discipline'))

    class Meta:
        managed = False
        db_table = 'direction_discipline'
        unique_together = (('direction_fk', 'discipline_fk'),)
        verbose_name = _('direction with disciplines')
        verbose_name_plural = _('directions with disciplines')
