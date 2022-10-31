from django.contrib import admin

from app_education.models import Direction, Discipline


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass

