# -*- coding: utf-8 -*-

# THIS IS FOR DEVELOPMENT ENVIRONMENT
# DO NOT USE IT IN PRODUCTION

# Create your own dev_local.py
# import * this module there and use it like this:
# python manage.py runserver --settings=project.settings.dev_local

from __future__ import unicode_literals

from .base import *


DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = True
# TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '\{\{%s\}\}'  # Some Django templates relies on this being the default

ADMINS = (('John', 'john@example.com'), )  # Log email to console when DEBUG = False

SECRET_KEY = "DEV"

ALLOWED_HOSTS = ['127.0.0.1', 'local.dev']

INSTALLED_APPS.extend([
    'huey.contrib.djhuey',
])

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES.update({
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'st_rate_limit': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spirit_rl_cache',
        'TIMEOUT': None
    }
})

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#ST_ORDERED_CATEGORIES = True
ST_MATH_JAX = True
ST_RATELIMIT_ENABLE = False

# debg toolbar
INTERNAL_IPS = ['127.0.0.1']

ST_TASK_MANAGER = 'huey'
ST_SEARCH_INDEX_UPDATE_HOURS = 1
HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'name': 'spirit',
    'filename': os.path.join(BASE_DIR, 'huey.sqlite3'),
    'immediate_use_memory': False,
    'immediate': False,
    'utc': True,
    'connection': {},
    'consumer': {
        'workers': os.cpu_count() * 2 + 1,
        'worker_type': 'thread',
        'initial_delay': 0.1,
        'backoff': 1.15,
        'max_delay': 10.0,
        'scheduler_interval': 1,
        'periodic': True,
        'check_worker_health': True,
        'health_check_interval': 1,
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'context': {
        'task': 'spirit.core.tasks.full_search_index_update',
        'schedule': 3600 * 24  # run once every 24hs
    }
}

#ST_STORAGE = 'spirit.core.storage.OverwriteFileSystemStorage'
ST_SITE_URL = 'http://127.0.0.1:8000/'

ST_HUEY_SCHEDULE = {
    'notify_weekly': {
        'minute': '0',
        'hour': '0',
        'day_of_week': '1'  # 0=Sunday, 6=Saturday
    }
}

ST_NGRAM_SEARCH = True
