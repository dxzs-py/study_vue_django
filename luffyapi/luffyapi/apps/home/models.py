from django.db import models

# Create your models here.
class Banner(models.Model):
    """轮播广告图模型"""
    # 模型字段
    title = models.CharField(max_length=500,verbose_name="广告标题")
    link = models.CharField(max_length=500,verbose_name="广告链接")
    image_url = models.CharField(max_length=255, verbose_name='广告图片')
    remark= models.TextField(verbose_name='备注信息')
    is_show = models.BooleanField(default=True,verbose_name='是否显示')
    order = models.IntegerField(default=1,verbose_name='排序')
    is_deleted = models.BooleanField(default=False,verbose_name='是否删除')

    # 表信息声明
    class Meta:
        db_table = 'banner'
        verbose_name = '轮播广告图'
        verbose_name_plural = verbose_name


    # 自定义方法【自定义字段或者自定义工具方法】
    def __str__(self):
        return self.title