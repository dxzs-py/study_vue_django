from rest_framework import serializers
from .models import Order, OrderDetail
from django_redis import get_redis_connection
import datetime
from course.models import Course, CourseExpire


class OrderModelSerializer(serializers.ModelSerializer):
    """
    订单的序列化器
    """

    class Meta:
        model = Order
        fields = ["id", "order_number", "pay_type", "credit", "coupon"]
        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},
            "credit": {"write_only": True},
            "coupon": {"write_only": True}
        }

    def validate(self, attrs):
        # 验证数据

        pay_type = attrs.get("pay_type")
        try:
            Order.pay_choices[int(pay_type)]
        except:
            raise serializers.ValidationError({"message": "支付类型错误"})

        # todo 判断积分使用是否上限

        # todo 优惠券是否存在或者过期，是否满足使用条件

        # todo 校验购买的商品是否存在

        # 一定要return验证结果
        return attrs

    def create(self, validated_data):
        """生成订单[使用事务来完成订单的生成]"""

        # 调用序列化器 OrderSerializer(instance="模型对象",data=data,context={"views":"视图对象(self)","request":"请求对象(self.request)","format":"客户端上传过来的数据格式(self.format_kwarg)"})
        user_id = 1 #self.context["request"].user.id

        # 生成唯一的订单号[结合时间+用户ID+随机数(递增值<redis中针对一个数值不断递增>)]
        redis_conn = get_redis_connection("cart")
        incr = int(redis_conn.incr("order"))
        order_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr

        # 先 生成订单
        order = Order.objects.create(
            order_title="你购买课程",
            total_price=0,
            real_price=0,
            order_number=order_number,  # 订单号
            order_status=0,  # 进到这里都是选好未支付的
            pay_type=validated_data.get("pay_type"),
            credit=validated_data.get("pay_type", 0),
            coupon=validated_data.get("pay_type", 0),
            order_desc="",
            user_id=user_id  # 另外一种写法 user = self.context["request"].user // 因为user是模型对象，不能直接用user=user.id，需要用user_id
        )

        # 然后生成订单详情[记录本次下单的所有商品课程信息]

        cart_bytes_dict = redis_conn.hgetall("cart_%s" % user_id)
        selected_bytes_list = redis_conn.smembers("selected_%s" % user_id)

        # 获取勾选的商品
        for course_id_bytes, expire_id_bytes in cart_bytes_dict.items():
            course_id = int(course_id_bytes.decode())  # bytes转str,再从str转int
            expire_id = int(expire_id_bytes.decode())
            # 判断当前商品id是否在勾选集合中
            if course_id_bytes in selected_bytes_list:
                try:
                    course = Course.objects.get(id=course_id, is_show=True, is_deleted=False)
                except Course.DoesNotExist:
                    raise serializers.ValidationError({"message": "对不起，购买的商品不存在或者已经下架！"})
                # 判断课程，获取课程原价
                original_price = course.price
                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        original_price = course_expire.price
                except CourseExpire.DoesNotExist:
                    pass
                real_price = course.real_price(expire_id)
                OrderDetail.objects.create(
                    order=order,
                    course=course,
                    expire=expire_id,
                    price=original_price,
                    real_price=real_price,
                    discount_name=course.discount_name,
                )
                # 计算订单价格
                order.total_price += float(original_price)
                order.real_price += float(real_price)
        order.save()

        # 返回生成的模型
        return order
