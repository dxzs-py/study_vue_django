from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *

from luffyapi.settings.constants import *
# 在此处创建您的视图。
class BannerListAPIView(ListAPIView):
    """轮播广告图"""
    # 倒序order_by("-orders")
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("order",'-id')[:BANNER_LENGTH]
    serializer_class = BannerModelSerializer

class HeaderNavigationListAPIView(ListAPIView):
    """顶部导航菜单"""
    queryset = Navigation.objects.filter(is_show=True, is_deleted=False, position=1).order_by("-order",'-id')[:HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer

class FooterNavigationListAPIView(ListAPIView):
    """顶部导航菜单"""
    queryset = Navigation.objects.filter(is_show=True, is_deleted=False, position=2).order_by("-order",'-id')[:FOOTER_NAV_LENGTH]
    serializer_class = NavModelSerializer