from django.apps import AppConfig


class UserLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_login'
    verbose_name = "用户管理"

    def ready(self):
        # 注册信号处理器
        from . import signals  # 添加这行