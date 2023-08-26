"""
Django settings for MewTeam project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import secrets
import string
from pathlib import Path
import yaml

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(5mqw33-@znu^p5wr$#ipgex=yx0s&2xrob287dbksrpllb3h^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

with open("secrets.yaml", 'r') as f:
    SECRETS = yaml.safe_load(f)
with open("config.yaml", 'r') as f:
    CONFIG = yaml.safe_load(f)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
AVATAR_ROOT = os.path.join(MEDIA_ROOT, "avatar/")
MESSAGE_ROOT = os.path.join(MEDIA_ROOT, "message/")

MAX_AVATAR_FILE_SIZE = 4 * 1024 * 1024
MAX_MESSAGE_FILE_SIZE = 64 * 1024 * 1024
# WEB_HOST_MEDIA_URL = os.path.join('http://127.0.0.1:8000', MEDIA_URL[1:], 'avatar/')

# Application definition

INSTALLED_APPS = [
    'daphne',  # 确保位于顶部
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "team",
    "message",
    "project",
    'corsheaders',
    'rest_framework',
    'channels',
    'chat',
    'file'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MewTeam.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "MewTeam.wsgi.application"
# 设置ASGI应用
ASGI_APPLICATION = "MewTeam.asgi.application"

# 设置通道层的通信后台 - 本地测试用
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
# redis 生产环境
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': SECRETS['database']
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

################################################################################
# CORS - Headers
#

CORS_ORIGIN_ALLOW_ALL = True

# 进行发送邮件的设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = False  # 是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.yeah.net'  # 发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 25  # 发件箱的SMTP服务器端口

EMAIL_HOST_USER = SECRETS['email']['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = SECRETS['email']['EMAIL_HOST_PASSWORD']  # 这是授权码
