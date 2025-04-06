from django.contrib import admin
from django.urls import path, include,re_path

# 导入 simplejwt 提供的几个验证视图类
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# 引入自定义的视图类
from .views import MyObtainTokenPairView,CaptchaAPIView,UserAPIView,MobileAPIView,SmSAPIView

urlpatterns = [
    # DRF 提供的一系列身份认证的接口，用于在页面中认证身份，详情查阅DRF文档
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 获取Token的接口
    path('login/token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token有效期的接口
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r"captcha/",CaptchaAPIView.as_view(), name="captcha"),
    path(r"reg/",UserAPIView.as_view(),name='register'),
    re_path(r"mobile/(?P<mobile>1[3-9]\d{9}/?$)",MobileAPIView.as_view(),name='mobile'),
    re_path(r"sms/(?P<mobile>1[3-9]\d{9}/?$)",SmSAPIView.as_view(),name='mobile')
]
