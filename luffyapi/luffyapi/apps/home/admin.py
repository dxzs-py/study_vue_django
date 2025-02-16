from django.contrib import admin

# 在此处注册您的模型。

admin.site.site_header = '戴兴django学习后端'  # 设置header
admin.site.site_title = '戴兴学习后端'  # 设置title
admin.site.index_title = '戴兴django学习'

from .models import *
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ["title","order","is_show","is_deleted"]
admin.site.register(Banner,BannerModelAdmin)

class NavModelAdmin(admin.ModelAdmin):
    list_display=["title","link","is_show","is_site","position"]
admin.site.register(Navigation,NavModelAdmin)

