from abc import ABC, abstractmethod
from typing import List

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

from app_education.models import Discipline, Direction, DirectionDiscipline
from app_students.models import Class, Student


class PermissionBase(ABC):
    def __init__(self, *args, **kwargs):
        self.action = args
        name = self.model.__name__.lower()
        self._permissions = (
            (f'{action}_{name}', f'Can {action} {name}')
            for action in self.action)

    @property
    def permissions(self):
        return self._permissions


class PermissionDiscipline(PermissionBase):
    model = Discipline


class PermissionDirection(PermissionBase):
    model = Direction


class PermissionDirectionDiscipline(PermissionBase):
    model = DirectionDiscipline


class PermissionStudent(PermissionBase):
    model = Student


class PermissionClass(PermissionBase):
    model = Class


class FactoryPermissions():
    def __init__(self, *args):
        self.MODELS = {
            0: PermissionDiscipline(*args),
            1: PermissionDirection(*args),
            2: PermissionDirectionDiscipline(*args),
            3: PermissionStudent(*args),
            4: PermissionClass(*args)
        }

    def __call__(self, key):
        content_type = ContentType.objects.get_for_model(
            self.MODELS.get(key).model)

        permission_objs = [Permission(codename=permission[0],
                                      name=permission[1],
                                      content_type=content_type)
                           for permission in self.MODELS.get(key).permissions]

        Permission.objects.bulk_create(permission_objs)


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        factory = FactoryPermissions('view', 'delete', 'add', 'change')
        for key in factory.MODELS.keys():
            factory(key)
