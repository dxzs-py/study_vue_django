from django.urls import path, include, re_path
from .views import CartAPIview

urlpatterns = [
    # DRF 提供的一系列身份认证的接口，用于在页面中认证身份，详情查阅DRF文档
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 获取Token的接口
    path('', CartAPIview.as_view(
        {'post': 'add', 'get': 'list',
         'patch': 'change_selected', "put": "change_expire",
         "delete": "del_cart"},
    )),
    path("order/",CartAPIview.as_view(
        {"get": "get_selected_course"}
    ))

]
