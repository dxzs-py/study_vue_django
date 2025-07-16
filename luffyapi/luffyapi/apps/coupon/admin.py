from django.contrib import admin
from .models import Coupon
class CouponModelAdmin(admin.ModelAdmin):
    """优惠券模型管理类"""
    list_display = ["name","coupon_type","timer"]
admin.site.register(Coupon, CouponModelAdmin)


from .models import UserCoupon
class UserCouponModelAdmin(admin.ModelAdmin):
    """我的优惠券模型管理类"""
    list_display = ["user","coupon","start_time","is_use"]

admin.site.register(UserCoupon, UserCouponModelAdmin)