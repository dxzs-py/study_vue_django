from django.urls import path
from .views import BannerListAPIView

urlpatterns = [
    path('banner/', BannerListAPIView.as_view()) # 将类视图实例化，并返回一个可调用的视图函数。
]