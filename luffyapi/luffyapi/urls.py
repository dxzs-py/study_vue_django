"""
这段代码是Django项目的URL配置文件，定义了如何将URL映射到视图函数或类。urlpatterns列表用于路由URL到视图。更多信息请参阅： https://docs.djangoproject.com/en/5.1/topics/http/urls/ 示例：
    函数视图
        1.添加导入：from my_app import views
        2.将URL添加到urlpatterns：path('', views.home, name='home')
    类视图
        1.添加导入：from other_app.views import Home
        2.将URL添加到urlpatterns：path('', Home.as_view(), name='home')
    包含其他URL配置文件
        1.导入include()函数：from django.urls import include, path
        2.将URL添加到urlpatterns：path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path,include

from django.urls import re_path  # 导入正则表达式的路径处理函数
from django.conf import settings  # 导入Django设置模块，用于访问设置变量
from django.views.static import serve  # 导入用于服务静态文件的视图函数


# 定义URL模式的列表，用于将URL映射到相应的视图
"""
使用正则表达式匹配媒体文件的URL，并将其映射到serve函数
r'media/(?P<path>.*)' 表示匹配以'media/'开头后跟任意路径的URL
serve 是一个视图函数，用于服务静态文件
{"document_root": settings.MEDIA_ROOT} 是传递给serve函数的额外参数，指定媒体文件的根目录
"""
urlpatterns = [
    # 将以'admin/'开头的URL映射到Django自带的管理后台
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    path('', include('home.urls')),
    path('user/', include('user_login.urls')),
    path('course/', include('course.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('coupon/', include('coupon.urls')),
    path('payments/', include('payments.urls')),

]
