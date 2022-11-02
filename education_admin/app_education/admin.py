from django.contrib import admin

from app_education.models import Direction, Discipline, DirectionDiscipline


class DisciplineInLineAdmin(admin.TabularInline):
    """Добавление или изменение направления у дисциплины"""
    model = DirectionDiscipline


class DirectionInLineAdmin(admin.TabularInline):
    """Добавление или изменение дисциплин у направления"""
    model = DirectionDiscipline


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Панель для направлений подготовки"""
    list_display = ('name', 'curator_fk')
    list_filter = ('curator_fk',)
    list_select_related = ('curator_fk',)
    search_fields = ('name',)
    inlines = (DisciplineInLineAdmin, )


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    """Панель для дисциплин"""
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (DirectionInLineAdmin,)
