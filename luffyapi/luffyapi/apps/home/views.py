from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer

from luffyapi.settings.constants import *
# 在此处创建您的视图。
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("order",'-id')[:BANNER_LENGTH]
    # 倒序order_by("-orders")
    serializer_class = BannerModelSerializer