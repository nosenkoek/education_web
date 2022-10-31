from django.contrib import admin

from app_students.models import Class, Student


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
