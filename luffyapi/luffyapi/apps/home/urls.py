from django.urls import path
from . import views

urlpatterns = [
    path('banner/', views.BannerListAPIView.as_view()),  # 将类视图实例化，并返回一个可调用的视图函数。
    path('nav/header/', views.HeaderNavigationListAPIView.as_view()),
    path('nav/footer/', views.FooterNavigationListAPIView.as_view())

]
