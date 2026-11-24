"""
Django settings for coaching_project project.
"""

from pathlib import Path
import os
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if present
env_file = BASE_DIR / '.env'
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-coaching-mgmt-sys-secret-key-prod-2026'
)

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [
    host.strip() 
    for host in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver').split(',') 
    if host.strip()
]
if DEBUG:
    ALLOWED_HOSTS.extend(['*', 'testserver'])



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Project Application
    'coaching_core.apps.CoachingCoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coaching_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coaching_project.wsgi.application'


# Database Configuration
# Default target is MySQL. If MySQL is not running and USE_SQLITE is set or MySQL unreachable,
# a fallback to SQLite is provided so the project can be tested immediately.

def check_mysql_accessible(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        return result == 0
    except Exception:
        return False

db_engine_choice = os.environ.get('DB_ENGINE', 'mysql').lower()
use_sqlite_flag = os.environ.get('USE_SQLITE', '0').lower() in ('1', 'true', 'yes')

mysql_host = os.environ.get('DB_HOST', '127.0.0.1')
mysql_port = os.environ.get('DB_PORT', '3306')

if use_sqlite_flag or db_engine_choice == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # If explicitly forcing mysql or if mysql server socket is responding
    is_live = check_mysql_accessible(mysql_host, mysql_port)
    if is_live or os.environ.get('FORCE_MYSQL', '0') == '1':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('DB_NAME', 'coaching_db'),
                'USER': os.environ.get('DB_USER', 'root'),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': mysql_host,
                'PORT': mysql_port,
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        }
    else:
        # Graceful development fallback when MySQL server daemon is not started
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Messages Bootstrap mapping
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
