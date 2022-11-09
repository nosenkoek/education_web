import os

from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG') != 'True'

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

include(
    'components/database.py',
    'components/auth_password_validators.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/internationalization.py',
    'components/debug_toolbar_panels.py',
)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False
CELERY_TRACK_STARTED = True
CELERYD_LOG_FILE = os.path.join(
    BASE_DIR, 'celery', 'logs')
CELERYD_LOG_LEVEL = "INFO"

