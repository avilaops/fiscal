"""
Django settings for PRODUCTION deployment on Azure Container Instances
"""

import os
from .settings import *

# SECURITY
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Allowed hosts - lê da variável de ambiente
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', 'fiscal.avila.inc,*.azurecontainer.io')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]

# HTTPS/Security - Desabilitado para HTTP por enquanto
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database - MongoDB Atlas or SQLite
USE_MONGODB = os.environ.get('USE_MONGODB', 'false').lower() == 'true'

if USE_MONGODB:
    # MongoDB Configuration
    MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING', '')
    MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'aviladevops_fiscal')

    # Djongo configuration
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': MONGODB_DATABASE,
            'CLIENT': {
                'host': MONGODB_CONNECTION_STRING,
            }
        }
    }
else:
    # SQLite para testes
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# CORS - Em produção, especifique os domínios permitidos
CORS_ALLOWED_ORIGINS = [
    "http://fiscal.avila.inc",
    "http://fiscal.avila.inc:8000",
    "https://fiscal.avila.inc",
    "https://www.fiscal.avila.inc",
    "https://fiscal.aviladevops.com.br",
    "https://www.fiscal.aviladevops.com.br",
    "capacitor://localhost",
    "ionic://localhost",
]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "http://fiscal.avila.inc",
    "http://fiscal.avila.inc:8000",
    "https://fiscal.avila.inc",
    "http://*.azurecontainer.io",
    "http://*.azurecontainer.io:8000",
]

# Session timeout
SESSION_COOKIE_AGE = 86400  # 24 horas
