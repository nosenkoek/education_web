from abc import ABC

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import transaction

from app_education.models import Discipline, Direction, DirectionDiscipline
from app_students.models import Class, Student
from app_users.services.decorator import CollectionPermission


ACTIONS = ('view', 'delete', 'add', 'change')


class FactoryPermissions():
    MODELS = {}

    def __call__(self, key, actions):
        permission_class = self.MODELS.get(key)
        permission_obj = permission_class(*actions)
        content_type = ContentType.objects.get_for_model(permission_obj.model)

        permission_objs = [Permission(codename=permission[0],
                                      name=permission[1],
                                      content_type=content_type)
                           for permission in permission_obj.permissions]

        Permission.objects.bulk_create(permission_objs)


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


@CollectionPermission('discipline', FactoryPermissions.MODELS)
class PermissionDiscipline(PermissionBase):
    model = Discipline


@CollectionPermission('direction', FactoryPermissions.MODELS)
class PermissionDirection(PermissionBase):
    model = Direction


@CollectionPermission('directiondiscipline', FactoryPermissions.MODELS)
class PermissionDirectionDiscipline(PermissionBase):
    model = DirectionDiscipline


@CollectionPermission('student', FactoryPermissions.MODELS)
class PermissionStudent(PermissionBase):
    model = Student


@CollectionPermission('class', FactoryPermissions.MODELS)
class PermissionClass(PermissionBase):
    model = Class


class AddGroupMixin():
    @staticmethod
    def add_group_admin():
        group = Group.objects.create(name='Администратор')
        permissions = Permission.objects.all()
        group.permissions.set(permissions)
        group.save()

    @staticmethod
    def add_group_curator():
        group = Group.objects.create(name='Куратор')
        permissions = Permission.objects.filter(
            content_type__model__in=['class', 'student']).all()
        group.permissions.set(permissions)
        group.save()


class Command(BaseCommand, AddGroupMixin):
    help = 'Add teo groups (admin, curator) and add permission to these groups'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        factory = FactoryPermissions()
        for key in factory.MODELS.keys():
            factory(key, actions=ACTIONS)

        self.add_group_admin()
        self.add_group_curator()
