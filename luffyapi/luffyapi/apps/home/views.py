from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer
# Create your views here.
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("order",'-id')
    # 倒序order_by("-orders")
    serializer_class = BannerModelSerializer