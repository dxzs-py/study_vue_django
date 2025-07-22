from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r"alipay/", views.AlipayApiView.as_view()),
    path(r"alipay/result/", views.AliPayResultAPIView.as_view()),
]
