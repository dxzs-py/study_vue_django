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
    'rest_framework',  # 有很多功能，方便后面开发
    'rest_framework_simplejwt',
    'django_filters',
    'ckeditor',  # 富文本编辑器,核心应用
    'ckeditor_uploader',  # 富文本编辑器上传图片模块

    # 子应用
    'home',
    'user_login',
    'course',
    'cart',
    'order',
    'coupon',
    'payments'

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
    'luffyapi.middlewares.range_file_middleware.RangeFileMiddleware'
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

# 设置redis缓存
CACHES = {
    # 默认缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 项目上线时,需要调整这里的路径
        "LOCATION": "redis://127.0.0.1:6379/0",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供给admin或者admin的session存储
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供存储短信验证码
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供存储购物车信息
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

}

# 设置admin用户登录时,登录信息session保存到redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

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

# USE_TZ = True
USE_TZ = False  # 保证数据库中django中使用的时区一致！

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# 访问静态文件的url地址前缀
STATIC_URL = '/static/'
# 设置django的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

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

    # 默认认证类设置
    # 该配置项定义了API请求的身份验证机制，默认使用以下几种身份验证方式：
    # - JWTAuthentication：基于JSON Web Token (JWT) 的身份验证，通过rest_framework_simplejwt库实现。
    # - SessionAuthentication：基于会话的身份验证，适用于浏览器客户端。
    # - BasicAuthentication：基于HTTP基本认证的身份验证，适用于简单的API调用。
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],

    # 默认权限类设置
    # 该配置项定义了API请求的权限控制，默认要求用户必须通过身份验证才能访问受保护的API资源。
    # - IsAuthenticated：仅允许已通过身份验证的用户访问API。
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',  # 默认要求认证
        'rest_framework.permissions.AllowAny',  # 所有视图默认开放
    ],

}

# SimpleUI配置
# SIMPLEUI_CONFIG = {
#     "title": "LuffyCity",  # 修改标题
#     "site_title": "LuffyCity",  # 修改左上角标题
#     "site_footer": "LuffyCity",  # 修改页脚
#     "menu_style": "accordion",  # 菜单折叠
# }
SIMPLEUI_LOGO = ''  # 去掉默认Logo或换成自己Logo链接
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
# 项目中存储上传文件的根目录[暂时配置]，注意，uploads目录需要手动创建否则上传文件时报错
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
# 访问上传文件的url地址前缀
MEDIA_URL = "/media/"

# 注册自定义用户模型 值格式必须是“应用名.模型类名”
AUTH_USER_MODEL = 'user_login.User'

# simplejwt配置， 需要导入datetime模块
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),  # 访问令牌有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # 刷新令牌有效期
    'ROTATE_REFRESH_TOKENS': True,  # 刷新后使旧令牌失效
    'BLACKLIST_AFTER_ROTATION': True,  # 需安装 `rest_framework_simplejwt.token_blacklist`
    'ALGORITHM': 'HS256',  # 加密算法
    "TOKEN_OBTAIN_SERIALIZER": "user_login.serializers.MyTokenObtainPairSerializer",  # 自定义序列化器
}
# 实现多条件登录
AUTHENTICATION_BACKENDS = [
    'user_login.serializers.UsernameMobileAuthBackend'
]

SMS = {
    # 主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
    "_accountSid": "2c94811c946f6bfb0195f1708c154156",
    # 主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
    "_accountToken": "d6a9786cf13b4a25a9fbef299400993b",
    # 请使用管理控制台首页的APPID或自己创建应用的APPID
    "_appId": "2c94811c946f6bfb0195f1708db5415d",
    # 说明：请求地址，生产环境配置成app.cloopen.com
    # 沙箱环境地址： sandboxapp.cloopen.com
    "_serverIP": "sandboxapp.cloopen.com",
    # 说明：请求端口 ，生产环境为8883
    "_serverPort": "8883",
    # 说明：REST API版本号保持不变
    "_softVersion": "2013-12-26"
}

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'full',  # 工具条功能，full表示全部功能,Basic表示精简功能
        'toolbar': 'Custom',  # 自定义工具条
        'toolbar_Custom': [
            # cke_button_工具名称[注意改成驼峰式写进来]
            ['Bold', 'Italic', 'Underline', 'Image'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 400,  # 编辑器高度
        # 'width': 300,     # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，留空则调用django的文件上传功能
CKEDITOR_VERSION = '4.24.0-lts'  # 指定LTS版本

# 支付宝配置信息
ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do", # 真实支付宝网关地址
    "gateway_url": "https://openapi-sandbox.dl.alipaydev.com/gateway.do",  # 沙箱支付宝网关地址
    "appid": "9021000150658560",
    "app_notify_url": None,  # 支付宝异步通知地址
    "app_private_key_path": os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem"),
    "alipay_public_key_path": os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem"),
    "sign_type": "RSA2",
    "debug": False,
    "return_url": "http://www.luffycity.cn:8080/payments/result",  # 同步回调地址
    "notify_url": "http://api.luffycity.cn:8000/payments/result",  # 异步结果通知
}

# 保利威视频加密服务
POLYV_CONFIG = {
    "userId": "a8f20da824",
    "secretkey": "t1VqfGx5BH",
    "tokenUrl": "https://hls.videocc.net/service/v1/token",
}
