from rest_framework import serializers
from .models import UserCoupon,Coupon

class CouponModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["name","condition","coupon_type","timer","sale"]

class UserCouponModelSerializer(serializers.ModelSerializer):
    """
    课程分类序列化器
    """
    coupon = CouponModelSerializer()
    class Meta:
        model = UserCoupon
        fields = ["id","start_time","coupon","end_time"]

