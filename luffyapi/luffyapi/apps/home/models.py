from django.db import models
from luffyapi.utils.models import BaseModel
# 在此处创建您的模型。
class Status(models.TextChoices):
    """
    定义项目状态的选项类

    继承自models.TextChoices，为项目状态提供了一个固定的选项集合
    包含三种状态：未开始、进行中和已完成
    每个选项包括一个短代码（数据库存储用）和一个易读的描述
    """
    UNSTARTED = 'u', "Not started yet"  # 未开始状态
    ONGOING = 'o', "Ongoing"  # 进行中状态
    FINISHED = 'f', "Finished"  # 已完成状态


"""
 from third_package.models import ModelA

 ModelA._meta.verbose_name = ''
 ModelA._meta.verbose_name_plural = ''
 ModelA._meta.get_field('first_name').verbose_name = '名字'
"""


class Banner(BaseModel):
    """轮播广告图模型"""
    # 模型字段
    title = models.CharField(max_length=500, verbose_name="广告标题")
    link = models.CharField(max_length=500, verbose_name="广告链接")
    # upload_to 设置上传文件的保存子目录
    image_url = models.ImageField(upload_to="banner", null=True, blank=True, max_length=255, verbose_name="广告图片")
    remark = models.TextField(verbose_name='备注信息')

    # 表信息声明
    class Meta:
        db_table = 'banner'
        verbose_name = '轮播广告图'
        verbose_name_plural = verbose_name

    # 自定义方法【自定义字段或者自定义工具方法】
    def __str__(self):
        return self.title


class Navigation(BaseModel):
    """导航菜单模型模型"""
    # 模型字段
    POSITION_OPTION = (
        (1, '顶部导航'),
        (2, '底部导航'),
    )

    title = models.CharField(max_length=500, verbose_name="导航标题")
    link = models.CharField(max_length=500, verbose_name="导航链接")
    position = models.IntegerField(default=1, verbose_name='导航位置',choices=POSITION_OPTION)
    is_site = models.BooleanField(default=False, verbose_name='是否站外地址')

    class Meta:
        db_table = 'ly_nav'
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name

    # 自定义方法
    def __str__(self):
        return self.title