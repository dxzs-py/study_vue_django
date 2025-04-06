from django.db import models
from django.contrib.auth.models import AbstractUser # 这个类包含了用户名，密码等很多字段，所以直接继承就可以


# Create your models here.
class User(AbstractUser):
    # 自定义字段
    mobile = models.CharField(max_length=15, unique=True, verbose_name="手机号")
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name="用户头像")
    wechat = models.CharField(max_length=64, null=True, blank=True, verbose_name="微信号")
    class Meta:
        db_table = "ly_users"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
