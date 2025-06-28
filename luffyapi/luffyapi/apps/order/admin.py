from django.contrib import admin
from .models import Order
class OrderModelAdmin(admin.ModelAdmin):
    """订单模型管理类"""
    pass


admin.site.register(Order, OrderModelAdmin)

from .models import OrderDetail
class OrderDetailModelAdmin(admin.ModelAdmin):
    """订单详情模型管理类"""
    pass

admin.site.register(OrderDetail, OrderDetailModelAdmin)