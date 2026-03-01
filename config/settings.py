import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-l^u%blr5+r0qjvn64af*&i6w*m7x%!_n!%0meogo1$+71d0*5c'

DEBUG = True

ALLOWED_HOSTS = ["*"] #allow everything for now in dev

# ---------------------------------
# Application definition
# ---------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #local apps
    'authcore',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# ---------------------------------
# Database → PostgreSQL (Docker-ready)
# ---------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        # service name in docker-compose
        'HOST': "db",
        'PORT': os.getenv("POSTGRES_PORT", "5432"),
    }
}


# ---------------------------------
# Password validation
# ---------------------------------

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


# ---------------------------------
# Internationalization
# ---------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ---------------------------------
# Static files (CSS, JavaScript, Images)
# ---------------------------------

STATIC_URL = 'static/'

# ---------------------------------
# Celery
# ---------------------------------
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
