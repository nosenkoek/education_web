from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppStudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_students'
    verbose_name = _('students')
