"""
Django settings for meetingroot project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bp(w-(!)pwey*0y+2lugb1zsu)inx1%m*%=ljuq^zjq#9pfp6y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'bootstrap4',
    'registration',  # should be immediately above 'django.contrib.admin'
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_python3_ldap',
    'jobs',
    'interview',
]

MIDDLEWARE = [
    'interview.performance.performance_logger_middleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meetingroot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'jobs/templates',
                 BASE_DIR / 'interview/templates',
                 BASE_DIR / 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meetingroot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # LDAP
# # The URL of the LDAP server.
# LDAP_AUTH_URL = "ldap://localhost:389"
# # Initiate TLS on connection.
# LDAP_AUTH_USE_TLS = False
#
# # The LDAP search base for looking up users.
# LDAP_AUTH_SEARCH_BASE = "dc=ihopeit,dc=com"
# # The LDAP class that represents a user.
# LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"
#
# # User model fields mapped to the LDAP
# # attributes that represent them.
# LDAP_AUTH_USER_FIELDS = {
#     "username": "cn",
#     "first_name": "givenName",
#     "last_name": "sn",
#     "email": "mail",
# }
#
# # A tuple of django model fields used to uniquely identify a user.
# LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
#
# # Path to a callable that takes a dict of {model_field_name: value},
# # returning a dict of clean model data.
# # Use this to customize how data loaded from LDAP is saved to the User model.
# LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
#
# # The LDAP username and password of a user for querying the LDAP database for user
# # details. If None, then the authenticated user will be used for querying, and
# # the `ldap_sync_users` command will perform an anonymous query.
# LDAP_AUTH_CONNECTION_USERNAME = None
# LDAP_AUTH_CONNECTION_PASSWORD = None
#
# # LDAP login authentication
# AUTHENTICATION_BACKENDS = {"django_python3_ldap.auth.LDAPBackend",'django.contrib.auth.backends.ModelBackend',}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {  # 供后面formatter进行选择
        'verbose': {  # 定义长格式
            'format': '{levelname} {asctime} {module} {lineno} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {  # 定义短格式
            'format': '{levelname} {asctime} {name} {lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {  # 供后面handlers进行选择
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        "mail_admins": {
            "level": 'ERROR',
            "class": "django.utils.log.AdminEmailHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": BASE_DIR / 'recruitment.admin.log',
        },
        'performance': {
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': BASE_DIR / 'recruitment.performance.log',
        },
    },

    # 'root': {
    #     'handlers': ['console', 'file'],
    #     'level': 'INFO',
    # },

    "loggers": {
        "django.db.backends": {  # 指定日志记录器
            "handlers": ["file"],  # 指定日志处理方法
            "level": "DEBUG",  # 指定日志级别
        },
        # "django_python3_ldap": {
        #     "handlers": ["console", "file"],
        #     "level": "DEBUG",
        # },
        "interview.performance": {
            "handlers": ["console", "performance"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# dingding

DINGTALK_WEB_HOOK = 'https://oapi.dingtalk.com/robot/send?access_token=688d5e0b585baddc70dba45d0c75b924021b31189b71c09b635e918076837ce0'

# Django-Registration-Redux

# 设为 True，允许用户注册
REGISTRATION_OPEN = True
# 关闭注册时重定向到LOGIN_REDIRECT_URL，先完成注册
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = False
# 注册成功后重定向
SIMPLE_BACKEND_REDIRECT_URL = '/accounts/login/'
# 登录成功后重定向
LOGIN_REDIRECT_URL = '/'
