from django.db import models

class BaseModel(models.Model):
    """基础模型"""
    # 模型字段
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    order = models.IntegerField(default=1, verbose_name='排序')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True  # 设置当前模型为抽象模型，在数据迁移的时候django就不会为它单独创建一张表