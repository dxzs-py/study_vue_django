from django.contrib import admin

# 在此处注册您的模型。

admin.site.site_header = '戴兴django学习后端'  # 设置header
admin.site.site_title = '戴兴学习后端'  # 设置title
admin.site.index_title = '戴兴django学习'

from .models import Banner,Navigation
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ["title","order","is_show","is_deleted"]
admin.site.register(Banner,BannerModelAdmin)

class NavModelAdmin(admin.ModelAdmin):
    list_display=["title","link","is_show","is_site","position"]
admin.site.register(Navigation,NavModelAdmin)

# from luffyapi.apps.user_login.models import User
# class UserModelAdmin(admin.ModelAdmin):
#     """
#     UserModelAdmin类继承自admin.ModelAdmin，用于定制用户模型在管理员界面的显示和操作。
#     该类设置了用户列表的显示字段、过滤条件、搜索字段、每页显示数量、排序方式以及可编辑字段，
#     并组织了用户信息的基本显示格式。
#     """
#
#     # 设置用户列表显示的字段
#     list_display = ["username", "email", "mobile",]
#
#     # 设置用户列表的过滤条件
#     list_filter = ["is_superuser"]
#
#     # 设置用户列表的搜索字段
#     search_fields = ["username", "email", "mobile"]
#
#     # 设置每页显示的用户数量
#     list_per_page = 10
#
#     # 设置用户列表的排序方式，按ID降序排列
#     ordering = ["-id"]
#
#     # 设置用户列表中可直接编辑的字段
#     list_editable = ["is_superuser"]
#
#     # 设置用户信息的字段集，将用户信息分为基本信息部分
#     fieldsets = (
#         ("基本信息", {
#             "fields": ("username", "password", "email", "mobile"),
#         })
#     )
#
#
# admin.site.register(User, UserModelAdmin)
