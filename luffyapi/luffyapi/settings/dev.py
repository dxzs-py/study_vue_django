"""
luffyapi 项目的 Django 设置。

由 'django-admin startproject' 使用 Django 5.1.6 生成。

有关此文件的更多信息，请参阅
https://docs.djangoproject.com/en/5.1/topics/settings/

有关设置及其值的完整列表，请参阅
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# 在项目内构建路径，如下所示： BASE_DIR / 'subdir'。
BASE_DIR = Path(__file__).resolve().parent.parent
"""
等价于
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR 项目的主应用目录
"""

# 把apps目录下面的所有子应用设置为可以直接导包，那就需要把apps设置为默认导包路径
import sys
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
import home
"""
因为sys.path默认送不含有该路径的，这样送在sys.path中添加一个路径。
但是pycharm还是会认为导包失败
这样就不用from luffyapi.apps import home这么长的写导包
"""


# 快速启动开发设置 - 不适合生产
# 查看 https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wp(a!sv^o5tq_g(u!iper(kydhbexg^*aa*y$9xhy5wx+ozw4-'

# 安全警告：请勿在生产环境中开启调试的情况下运行！
DEBUG = True

ALLOWED_HOSTS = [
    "api.luffycity.cn",
    "www.luffycity.cn"
]

# 应用程序定义
INSTALLED_APPS = [
    'simpleui',  # 必须放在 admin 之前
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',  # 跨域请求,需要配置CORS_ORIGIN_WHITELIST
    'rest_framework', # 有很多功能，方便后面开发

    # 子应用
    'home',
]

# CORS组的配置信息
CORS_ORIGIN_WHITELIST = (
    # 在部分的cors_headrs模块中，如果不带协议，会导致客户端无法跨越，就需要配置"http://www.luffycity.cn:8080"
    'http://www.luffycity.cn:8080',
)
CORS_ALLOW_CREDENTIALS = False  # 是否允许ajax跨域请求时携带cookie

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域请求

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luffyapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'luffyapi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3', # 可以当做离线数据库
    # }
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "luffy_user",
        "PASSWORD": "luffy",
        "NAME": "luffy",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# 更改默认语言为中文
LANGUAGE_CODE = 'zh-hans'

# 修改时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# 访问静态文件的url地址前缀
STATIC_URL = '/static/'
# 设置django的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]

# 项目中存储上传文件的根目录[暂时配置]，注意，uploads目录需要手动创建否则上传文件时报错
MEDIA_ROOT=os.path.join(BASE_DIR, "uploads")
# 访问上传文件的url地址前缀
MEDIA_URL ="/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 日志配置
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 日志格式
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    # 过滤器
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    # 处理方式
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/luffy.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose'
        },
    },
    # 日志对象
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "propagate": True,  # # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    },
}

REST_FRAMEWORK = {  # 新加的配置
    # 异常处理
    'EXCEPTION_HANDLER': 'luffyapi.utils.exceptions.custom_exception_handler',  # 自己定义的异常处理
}

# SimpleUI配置
SIMPLEUI_LOGO = ''  # 去掉默认Logo或换成自己Logo链接
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
