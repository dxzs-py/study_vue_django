# Register your models here.
from django.contrib import admin
from .models import User,Credit


class UserModelAdmin(admin.ModelAdmin):
    """
    UserModelAdmin类继承自admin.ModelAdmin，用于定制用户模型在管理员界面的显示和操作。
    该类设置了用户列表的显示字段、过滤条件、搜索字段、每页显示数量、排序方式以及可编辑字段，
    并组织了用户信息的基本显示格式。
    """

    # 设置用户列表显示的字段
    list_display = ["username", "email", "wechat", "mobile", "is_active", "is_staff", "is_superuser", "credit"]

    # 设置用户列表的过滤条件
    list_filter = ["is_active", "is_staff", "is_superuser"]

    # 设置用户列表的搜索字段
    search_fields = ["username", "email", "mobile"]

    # 设置每页显示的用户数量
    list_per_page = 10

    # 设置用户列表的排序方式，按ID降序排列
    ordering = ["-id"]

    # 设置用户列表中可直接编辑的字段
    list_editable = ["is_active", "is_staff", "is_superuser", "wechat", "credit"]

    # 设置用户信息的字段集，将用户信息分为基本信息部分
    fieldsets = (
        ("基本信息", {
            "fields": ("username", "email", "mobile", "wechat", "credit"),
        }),
        ("权限信息", {
            "fields": ("is_active", "is_staff", "is_superuser"),
        }),
    )

    # def save_model(self, request, obj, form, change):
    #     """
    #     重写save_model方法，在保存User实例时自动记录积分变化
    #     """
    #     # 如果是修改操作（change=True）且对象已存在
    #     if change and obj.pk:
    #         # 获取数据库中当前的User对象
    #         old_obj = self.model.objects.get(pk=obj.pk)
    #         old_credit = old_obj.credit
    #         new_credit = obj.credit
    #
    #         # 检查积分是否发生变化
    #         if old_credit != new_credit:
    #             # 计算积分变化量
    #             credit_diff = new_credit - old_credit
    #
    #             # 确定操作类型（赚取或消费）
    #             opera = 0 if credit_diff > 0 else 1
    #             number = abs(credit_diff)
    #
    #             # 创建积分流水记录
    #             Credit.objects.create(
    #                 user=obj,
    #                 opera=opera,
    #                 number=number
    #             )
    #
    #     # 调用父类的save_model方法保存User对象
    #     super().save_model(request, obj, form, change)


admin.site.register(User, UserModelAdmin)


class CreditModelAdmin(admin.ModelAdmin):
    """积分流水管理类"""
    pass


admin.site.register(Credit, CreditModelAdmin)