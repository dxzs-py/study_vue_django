from django.urls import path
from .views import *

urlpatterns = [
    path('banner/', BannerListAPIView.as_view()),  # 将类视图实例化，并返回一个可调用的视图函数。
    path('nav/header/', HeaderNavigationListAPIView.as_view()),
    path('nav/footer/', FooterNavigationListAPIView.as_view())

]
