import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/database.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/auth_password_validators.py',
    'components/celery_settings.py',
    # 'components/logging.py'
)

AUTH_USER_MODEL = "users.User"

AUTH_API_LOGIN_URL = os.environ.get('AUTH_LOGIN_URL')

AUTHENTICATION_BACKENDS = [
    'users.auth.AuthBackend',
]

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

LOCALE_PATHS = ['notifications/locale']

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

NOTIFICATION_API = os.environ.get('NOTIFICATION_API')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
