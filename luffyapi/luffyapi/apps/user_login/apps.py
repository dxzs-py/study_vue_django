from django.apps import AppConfig


class UserLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_login'
    verbose_name = "用户管理"