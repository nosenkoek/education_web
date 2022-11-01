from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from app_students.models import Class, Student


class StudentInLineAdmin(admin.TabularInline):
    """Просмотр и удаление студентов в группе"""
    model = Student
    fields = ('full_name', 'email', 'tel_number', 'direction_fk')
    readonly_fields = fields
    list_select_related = ('direction_fk',)

    def get_queryset(self, request):
        queryset = super(StudentInLineAdmin, self).get_queryset(request)
        return queryset.select_related(*self.list_select_related)

    @admin.display(description=_('full name'))
    def full_name(self, obj):
        result = '<a href="{}">{}</a>'.format(
            reverse('admin:app_students_student_change',
                    args=(obj.id, )),
            obj.get_full_name())
        return mark_safe(result)

    def has_add_permission(self, request, obj) -> bool:
        """Возможность добавлять студентов"""
        return False


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """Панель для просмотра групп"""
    list_display = ('number', 'direction_fk', 'curator', 'free_place')
    readonly_fields = ('number',)
    list_select_related = ('direction_fk', )
    ordering = ('number',)
    inlines = (StudentInLineAdmin,)

    @admin.display(description=_('free places'))
    def free_place(self, obj) -> str:
        """Доп. поле свободных мест в группе"""
        return obj.free_place()

    @admin.display(description=_('free places'))
    def curator(self, obj) -> str:
        """Доп. поле свободных мест в группе"""
        return obj.direction_fk.curator_fk


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Панель для просмотра студентов и распределение их по группам"""
    list_display = ('full_name', 'tel_number', 'email', 'class_fk',
                    'direction_fk')
    list_select_related = ('class_fk', 'direction_fk')

    @admin.display(description=_('full name'))
    def full_name(self, obj) -> str:
        """Доп. поле отображения ФИО"""
        return obj.get_full_name()

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        result = super(StudentAdmin, self).render_change_form(
            request, context, add, change, form_url, obj
        )
        # Переопределение queryset для class_fk.
        # Возможность выбора группы только по направлению и
        # в случае свободного места
        context['adminform'].form.fields['class_fk'].queryset = \
            Class.objects.annotate(free_places=Count('student')) \
            .filter(direction_fk=obj.direction_fk, free_places__gte=0)
        return result
