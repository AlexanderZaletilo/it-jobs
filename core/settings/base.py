import os
import sys

from configurations import Configuration


class Base(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ALLOWED_HOSTS = ["*"]

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "292&qsne+7pl1u#h03@13**@tt^0debpa=2)mb$ue_*k@q+^+4"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    # Application definition
    sys.modules['django_dia'] = __import__('django-dia')

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "vacancies.apps.VacanciesConfig",
        "django_filters",
        "crispy_forms",
        "storages",
        "django_dia",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "core.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
                "libraries": {
                    "proper_paginate": "core.templatetags.proper_paginate",
                    "url_replace": "core.templatetags.url_replace",
                },
            },
        },
    ]

    WSGI_APPLICATION = "core.wsgi.application"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DATABASE_NAME"),
            "USER": os.environ.get("DATABASE_USER"),
            "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
            "HOST": os.environ.get("DATABASE_HOST"),
            "PORT": os.environ.get("DATABASE_PORT"),
            "CONN_MAX_AGE": 100,
            'OPTIONS': {'sslmode': 'require'},
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.1/topics/i18n/

    LANGUAGE_CODE = "ru-ru"

    TIME_ZONE = "Europe/Moscow"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.1/howto/static-files/

    STATIC_URL = "/static/"
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

    # AWS storage settings
    AWS_ACCESS_KEY_ID = os.environ.get("STORAGE_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.environ.get("STORAGE_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.environ.get("STORAGE_ENDPOINT_URL")
    AWS_S3_USE_SSL = True

    # S3 public media settings
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = AWS_S3_ENDPOINT_URL + f"/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "core.storage_backends.PublicMediaStorage"

    # S3 private media settings
    PRIVATE_MEDIA_LOCATION = "private"
    PRIVATE_FILE_STORAGE = "core.storage_backends.PrivateMediaStorage"

    # CORS SETTINGS
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True

    # CACHE
    REDIS_URL = "redis://{host}:{port}".format(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=os.environ.get("REDIS_PORT", 6379),
    )
    REDIS_CACHE_SETTINGS = {
        "BACKEND": "django_redis.cache.RedisCache",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
    CACHES = {
        "default": dict(LOCATION=REDIS_URL + "/0", **REDIS_CACHE_SETTINGS),
    }

    # CELERY STUFF
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = TIME_ZONE

    PROJECT_NAME = os.environ.get("PROJECT_NAME")

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "myformatter": {
                "format": "{levelname} {asctime} {module} {process:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "log.log",
                "formatter": "myformatter",
            },
        },
        "loggers": {
            "vacancies": {"handlers": ["file"], "level": "INFO", "propagate": True},
            "core": {"handlers": ["file"], "level": "INFO", "propagate": True},
        },
    }
    # CACHEOPS
    CACHEOPS_REDIS = REDIS_URL

    CACHEOPS = {
        "vacancies.Company": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.Specialty": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.Currency": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.SiteType": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.Vacancy": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.Application": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.StatusModel": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.GradeModel": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
        "vacancies.Resume": {
            "ops": "all",
            "timeout": int(os.environ.get("CACHEOPS_TIMEOUT", 600)),
        },
    }

    # MAILJET
    MAILJET_PUBLIC_KEY = os.environ.get("MAILJET_PUBLIC_KEY")
    MAILJET_PRIVATE_KEY = os.environ.get("MAILJET_PRIVATE_KEY")
    MAILJET_EMAIL_TEMPLATE_ID = int(os.environ.get("MAILJET_EMAIL_TEMPLATE_ID"))
    MAILJET_NOTIFICATION_TEMPLATE_ID = int(
        os.environ.get("MAILJET_NOTIFICATION_TEMPLATE_ID")
    )
