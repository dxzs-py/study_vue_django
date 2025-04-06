from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from rest_framework import permissions

from luffyapi.settings.constants import *
# 在此处创建您的视图。
class BannerListAPIView(ListAPIView):
    """轮播广告图"""
    # 倒序order_by("-orders")
    # permission_classes = [permissions.AllowAny]  # 允许任何人访问
    # permission_classes = [permissions.IsAuthenticated]  # 验证后才能访问，这个看需要设置
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("order",'-id')[:BANNER_LENGTH]
    serializer_class = BannerModelSerializer

class HeaderNavigationListAPIView(ListAPIView):
    """顶部导航菜单"""
    queryset = Navigation.objects.filter(is_show=True, is_deleted=False, position=1).order_by("-order",'-id')[:HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer

class FooterNavigationListAPIView(ListAPIView):
    """底部部导航菜单"""
    queryset = Navigation.objects.filter(is_show=True, is_deleted=False, position=2).order_by("-order",'-id')[:FOOTER_NAV_LENGTH]
    serializer_class = NavModelSerializer