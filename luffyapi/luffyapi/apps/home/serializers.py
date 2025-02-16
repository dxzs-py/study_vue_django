from rest_framework import serializers  # 序列化程序
from .models import Banner
class BannerModelSerializer(serializers.ModelSerializer):
    """轮播广告序列化器"""
    # 模型序列化器字段声明
    class Meta:
        model = Banner
        fields = ['link','image_url']  # 字段声明，要所有字段用 * 表示


from .models import Navigation
class NavModelSerializer(serializers.ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = Navigation
        fields = ["title","link","is_site"]